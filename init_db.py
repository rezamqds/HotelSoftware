#!/usr/bin/env python
"""Initialize database script."""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import init_db, reset_db

def main():
    """Initialize or reset database."""
    app = create_app()

    with app.app_context():
        if '--reset' in sys.argv:
            print("Resetting database...")
            reset_db()
            print("Database reset complete!")
        else:
            print("Initializing database...")
            init_db()
            print("Database initialized successfully!")

if __name__ == '__main__':
    main()
