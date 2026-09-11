from datetime import datetime

from models.db import get_db


class Room:
    """Room model for managing hotel rooms."""

    def __init__(self, room_id=None):
        self.id = room_id

    @staticmethod
    def create(room_data):
        """Create a new room."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                INSERT INTO rooms (room_number, room_type, capacity, price_per_night, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                room_data['room_number'], room_data['room_type'],
                room_data['capacity'], room_data['price_per_night'],
                room_data.get('description', '')
            ))

            conn.commit()
            room_id = cursor.lastrowid
            return room_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def get_all():
        """Get all rooms."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms ORDER BY room_number')
        rooms = cursor.fetchall()
        conn.close()
        return rooms

    @staticmethod
    def get_by_id(room_id):
        """Get room by ID."""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM rooms WHERE id = ?', (room_id,))
        room = cursor.fetchone()
        conn.close()
        return room

    @staticmethod
    def get_available(arrival_date=None, departure_date=None):
        """Get available rooms, optionally filtered by dates."""
        conn = get_db()
        cursor = conn.cursor()

        if arrival_date and departure_date:
            # Get rooms not occupied during the specified dates
            cursor.execute('''
                SELECT r.* FROM rooms r
                WHERE r.is_available = 1
                AND r.id NOT IN (
                    SELECT g.room_id FROM guests g
                    WHERE g.room_id IS NOT NULL
                    AND g.arrival_date < ? AND g.departure_date > ?
                )
                ORDER BY r.room_number
            ''', (departure_date, arrival_date))
        else:
            cursor.execute('SELECT * FROM rooms WHERE is_available = 1 ORDER BY room_number')

        rooms = cursor.fetchall()
        conn.close()
        return rooms

    @staticmethod
    def update(room_id, room_data):
        """Update room information."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE rooms SET
                    room_number = ?, room_type = ?, capacity = ?,
                    price_per_night = ?, is_available = ?, description = ?,
                    updated_at = ?
                WHERE id = ?
            ''', (
                room_data['room_number'], room_data['room_type'],
                room_data['capacity'], room_data['price_per_night'],
                room_data.get('is_available', 1), room_data.get('description', ''),
                datetime.now(), room_id
            ))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def delete(room_id):
        """Delete room."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            # Check if room has guests
            cursor.execute('SELECT COUNT(*) FROM guests WHERE room_id = ?', (room_id,))
            count = cursor.fetchone()[0]

            if count > 0:
                raise ValueError("Cannot delete room with assigned guests")

            cursor.execute('DELETE FROM rooms WHERE id = ?', (room_id,))
            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @staticmethod
    def update_availability(room_id, is_available):
        """Update room availability status."""
        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute('''
                UPDATE rooms SET is_available = ?, updated_at = ?
                WHERE id = ?
            ''', (is_available, datetime.now(), room_id))

            conn.commit()
            return cursor.rowcount > 0

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
