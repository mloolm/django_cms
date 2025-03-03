#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
from django.db import connections
from django.db.utils import OperationalError


def wait_for_db():
    db_conn = None
    max_retries = 10  # Максимальное количество попыток
    wait_time = 1  # Время ожидания между попытками в секундах
    retries = 0

    while not db_conn and retries < max_retries:
        try:
            db_conn = connections['default']
            db_conn.cursor()  # Проверка подключения
            print("Database is ready!")
        except OperationalError:
            retries += 1
            print(f"Database not ready, waiting {wait_time} second(s)... (Attempt {retries}/{max_retries})")
            time.sleep(wait_time)

    if not db_conn:
        print("Database not available after waiting. Exiting.")
        sys.exit(1)



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rs.settings')
    wait_for_db()
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
