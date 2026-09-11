# Gunicorn configuration
# NOTE: On Windows it is recommended to run via `start.bat` or `python run.py`
import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1
bind = '0.0.0.0:7331'  # Replace with your desired IP address and port
