import os

from flask import current_app

from models.db import get_db
from models.guest import Guest
from models.room import Room

__all__ = ['get_db', 'init_db', 'reset_db', 'Guest', 'Room']


def init_db():
    """Create tables (rooms, guests) if they do not exist."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_number TEXT UNIQUE NOT NULL,
            room_type TEXT NOT NULL,
            capacity INTEGER NOT NULL DEFAULT 1,
            price_per_night REAL NOT NULL,
            is_available INTEGER DEFAULT 1,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS guests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_foreign TEXT NOT NULL,
            room_id INTEGER,
            nationality TEXT,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            father_name TEXT,
            national_id TEXT,
            passport_number TEXT,
            gender TEXT,
            date_of_birth TEXT,
            phone_number TEXT,
            leader_name TEXT,
            leader_phone TEXT,
            arrival_date TEXT NOT NULL,
            departure_date TEXT NOT NULL,
            occupation TEXT,
            payment_type TEXT,
            payment_type TEXT,
            advance_payment REAL DEFAULT 0,
            balance REAL DEFAULT 0,
            total_amount REAL DEFAULT 0,
            note TEXT,
            is_companion INTEGER DEFAULT 0,
            primary_guest_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES rooms(id),
            FOREIGN KEY (primary_guest_id) REFERENCES guests(id)
        )
    ''')

    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_guests_room_id ON guests(room_id)'
    )
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_guests_primary_guest '
        'ON guests(primary_guest_id)'
    )
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_guests_national_id ON guests(national_id)'
    )
    cursor.execute(
        'CREATE INDEX IF NOT EXISTS idx_guests_passport ON guests(passport_number)'
    )

    conn.commit()
    conn.close()


def reset_db():
    """Delete the database file and recreate the schema (dev/testing only)."""
    db_path = current_app.config['DATABASE_PATH']
    if os.path.exists(db_path):
        os.remove(db_path)
    init_db()
