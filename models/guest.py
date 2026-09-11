from datetime import datetime

from models.db import get_db


class Guest:
    """Guest model for managing hotel guests."""

    def __init__(self, guest_id=None):
        self.id = guest_id

    @staticmethod
    def create(guest_data):
        """Create a new guest."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO guests (
                    is_foreign, room_id, nationality, name, last_name, father_name,
                    national_id, passport_number, gender, date_of_birth, phone_number,
                    leader_name, leader_phone, arrival_date, departure_date, occupation,
                    payment_type, advance_payment, balance, total_amount, note,
                    is_companion, primary_guest_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                guest_data['is_foreign'], guest_data.get('room_id'),
                guest_data.get('nationality', ''), guest_data['name'], guest_data['last_name'],
                guest_data.get('father_name', ''), guest_data.get('national_id', ''),
                guest_data.get('passport_number', ''), guest_data.get('gender', ''),
                guest_data.get('date_of_birth', ''), guest_data.get('phone_number', ''),
                guest_data.get('leader_name', ''), guest_data.get('leader_phone', ''),
                guest_data['arrival_date'], guest_data['departure_date'],
                guest_data.get('occupation', ''), guest_data.get('payment_type', ''),
                guest_data.get('advance_payment', 0), guest_data.get('balance', 0),
                guest_data.get('total_amount', 0), guest_data.get('note', ''),
                guest_data.get('is_companion', 0), guest_data.get('primary_guest_id')
            ))

            conn.commit()
            guest_id = cursor.lastrowid
            return guest_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Get all guests with room information."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT g.*, r.room_number, r.room_type
            FROM guests g
            LEFT JOIN rooms r ON g.room_id = r.id
            WHERE g.is_companion = 0
            ORDER BY g.created_at DESC
        ''')

        guests = cursor.fetchall()
        conn.close()
        return guests

    @staticmethod
    def get_by_id(guest_id):
        """Get guest by ID with companions."""
        conn = get_db()
        cursor = conn.cursor()

        # Get main guest
        cursor.execute('''
            SELECT g.*, r.room_number, r.room_type
            FROM guests g
            LEFT JOIN rooms r ON g.room_id = r.id
            WHERE g.id = ?
        ''', (guest_id,))

        guest = cursor.fetchone()
        if not guest:
            conn.close()
            return None

        # Get companions
        cursor.execute('''
            SELECT * FROM guests
            WHERE primary_guest_id = ?
            ORDER BY id
        ''', (guest_id,))

        companions = cursor.fetchall()
        conn.close()

        return {
            'guest': dict(guest),
            'companions': [dict(c) for c in companions]
        }

    @staticmethod
    def update(guest_id, guest_data):
        """Update guest information."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE guests SET
                    is_foreign = ?, room_id = ?, nationality = ?, name = ?,
                    last_name = ?, father_name = ?, national_id = ?,
                    passport_number = ?, gender = ?, date_of_birth = ?,
                    phone_number = ?, leader_name = ?, leader_phone = ?,
                    arrival_date = ?, departure_date = ?, occupation = ?,
                    payment_type = ?, advance_payment = ?, balance = ?,
                    total_amount = ?, note = ?, updated_at = ?
                WHERE id = ?
            ''', (
                guest_data['is_foreign'], guest_data.get('room_id'),
                guest_data.get('nationality', ''), guest_data['name'], guest_data['last_name'],
                guest_data.get('father_name', ''), guest_data.get('national_id', ''),
                guest_data.get('passport_number', ''), guest_data.get('gender', ''),
                guest_data.get('date_of_birth', ''), guest_data.get('phone_number', ''),
                guest_data.get('leader_name', ''), guest_data.get('leader_phone', ''),
                guest_data['arrival_date'], guest_data['departure_date'],
                guest_data.get('occupation', ''), guest_data.get('payment_type', ''),
                guest_data.get('advance_payment', 0), guest_data.get('balance', 0),
                guest_data.get('total_amount', 0), guest_data.get('note', ''),
                datetime.now(), guest_id
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(guest_id):
        """Delete guest and companions."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            # Delete companions first
            cursor.execute('DELETE FROM guests WHERE primary_guest_id = ?', (guest_id,))

            # Delete main guest
            cursor.execute('DELETE FROM guests WHERE id = ?', (guest_id,))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def search(search_term):
        """Search guests by name, national ID, or passport."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT g.*, r.room_number, r.room_type
            FROM guests g
            LEFT JOIN rooms r ON g.room_id = r.id
            WHERE (g.name LIKE ? OR g.last_name LIKE ? OR g.national_id LIKE ? OR g.passport_number LIKE ?)
            AND g.is_companion = 0
            ORDER BY g.created_at DESC
        ''', (f'%{search_term}%',) * 4)

        guests = cursor.fetchall()
        conn.close()
        return guests
