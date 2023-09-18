@echo off

rem Activate the virtual environment
call .venv\Scripts\activate

rem Start the Gunicorn server
gunicorn -c gunicorn_config.py app:app
