#!/usr/bin/env python
"""One-time migration: old flat guests schema -> new normalized schema.

The legacy `guests` table stores companions as flat rows with a `relation`
column. The new schema replaces `relation` with `is_companion` +
`primary_guest_id`, and drops `residence_unit` (rooms are a separate table).

Mapping applied:
  - relation non-empty  -> is_companion=1 (kept as-is; primary linkage isn't
                           recoverable without more info)
  - relation empty       -> is_companion=0 (primary guest)
  - residence_unit       -> preserved verbatim in `note` if the row has no note

Usage:
    python migrate.py                # migrate files/gs.mqds (backs up first)
    python migrate.py --dry-run      # report only, no writes

Safe: creates a timestamped backup under files/rawDB/ before touching data.
"""
import os
import sys
import shutil
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app            # noqa: E402
from models import init_db, get_db    # noqa: E402


def backup(db_path):
    """Copy the db file to files/rawDB/ with a timestamp."""
    raw_dir = os.path.join(os.path.dirname(db_path), 'rawDB')
    os.makedirs(raw_dir, exist_ok=True)
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(os.path.basename(db_path))
    dest = os.path.join(raw_dir, f'{name}_premigrate_{stamp}{ext}')
    shutil.copy2(db_path, dest)
    return dest


def migrate(db_path):
    app = create_app('development')
    app.config['DATABASE_PATH'] = db_path
    dry = '--dry-run' in sys.argv

    with app.app_context():
        conn = get_db()
        cur = conn.cursor()

        legacy_exists = cur.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='guests'"
        ).fetchone() is not None
        if not legacy_exists:
            print("No legacy guests table found; nothing to migrate.")
            conn.close()
            return

        cols = [r[1] for r in cur.execute("PRAGMA table_info(guests)").fetchall()]
        already_migrated = 'primary_guest_id' in cols and 'is_companion' in cols
        if already_migrated:
            print("guests table already has new columns; nothing to migrate.")
            conn.close()
            return

        if 'relation' not in cols or 'residence_unit' not in cols:
            print("Unexpected legacy schema; aborting to avoid data loss.")
            conn.close()
            return

        legacy = cur.execute(
            "SELECT is_foreign, relation, nationality, name, last_name, father_name, "
            "national_id, passport_number, gender, date_of_birth, phone_number, "
            "arrival_date, departure_date, residence_unit, leader_name, leader_phone, "
            "occupation, payment_type, advance_payment, balance, total_amount, note "
            "FROM guests"
        ).fetchall()
        print(f"Found {len(legacy)} legacy guest rows to migrate.")

        print("Backing up database...")
        if dry:
            print("  (dry-run, backup skipped)")
        else:
            dest = backup(db_path)
            print(f"  {dest}")

        if dry:
            conn.close()
            return

        cur.execute("DROP TABLE IF EXISTS guests")
        conn.commit()
        conn.close()

        init_db()

        conn = get_db()
        cur = conn.cursor()
        insert_sql = (
            "INSERT INTO guests (is_foreign, nationality, name, last_name, father_name, "
            "national_id, passport_number, gender, date_of_birth, phone_number, "
            "arrival_date, departure_date, leader_name, leader_phone, occupation, "
            "payment_type, advance_payment, balance, total_amount, note, is_companion) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        )
        for row in legacy:
            (
                is_foreign, relation, nationality, name, last_name, father_name,
                national_id, passport_number, gender, date_of_birth, phone_number,
                arrival_date, departure_date, residence_unit, leader_name, leader_phone,
                occupation, payment_type, advance_payment, balance, total_amount, note,
            ) = row
            is_comp = 1 if relation else 0
            if not note and residence_unit:
                note = f"واحد اقامت: {residence_unit}"
            cur.execute(insert_sql, (
                is_foreign, nationality, name, last_name, father_name,
                national_id, passport_number, gender, date_of_birth, phone_number,
                arrival_date, departure_date, leader_name, leader_phone,
                occupation, payment_type, advance_payment, balance, total_amount,
                note, is_comp,
            ))
        conn.commit()
        conn.close()
        print(f"Migrated {len(legacy)} rows into new schema.")


if __name__ == '__main__':
    migrate(os.path.join(os.getcwd(), 'files', 'gs.mqds'))
