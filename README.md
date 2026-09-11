# HotelSoftware

A hotel management system for managing guest registrations, rooms, dates, and payments. Supports both Iranian and foreign guests with a Persian (Farsi) interface.

## Features

- **Dual guest registration** — Iranian guests (national ID, father name) and foreign guests (passport, nationality, leader info)
- **Companion management** — add up to 8 companions per primary guest, stored as linked records
- **Dynamic room management** — create/edit/delete rooms, set capacity and price, track availability
- **Date-based availability** — check room availability between arrival/departure dates via API
- **Search** — find guests by name, national ID, or passport number
- **Persian digit handling** — Farsi/Arabic digits in form inputs convert to English server-side before DB save

## Tech Stack

Python · Flask (application factory pattern) · SQLite · Jinja2

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create the database schema (creates files/gs.mqds)
python init_db.py

# 3. If upgrading from the old flat schema, migrate existing data (backs up first)
python migrate.py

# 4. Run the app
python run.py
# → http://localhost:7331
```

## Project Layout

```
run.py            Entry point (app factory)
app/              Flask app: create_app() + blueprints + error handlers
models/           SQLite data layer (Guest, Room models, db connection)
utils/            Helpers (Persian→English digit conversion)
templates/        Jinja2 templates (base, form, list, rooms/, errors/)
config.py         Env-driven configuration (see .env.example)
init_db.py        Schema creation
migrate.py        Legacy-schema → new-schema one-time migration
```

## Commands

| Purpose | Command |
| --- | --- |
| Run dev server | `python run.py` |
| Init schema | `python init_db.py` |
| Reset DB (dev) | `python init_db.py --reset` |
| Migrate legacy data | `python migrate.py` |
| Lint | `pylint $(git ls-files '*.py')` |
| Production (Gunicorn) | `gunicorn -c gunicorn_config.py run:app` (or `start.bat`) |

## License

Free to use. If you wish to use it, buy the author a pizza :)

Made by [@rezamqds](https://github.com/rezamqds).