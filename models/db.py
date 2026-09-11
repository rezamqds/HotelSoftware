import sqlite3

from flask import current_app


def get_db():
    """Get a database connection to the configured SQLite file."""
    db_path = current_app.config['DATABASE_PATH']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn
