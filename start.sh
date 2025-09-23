#!/bin/bash

# Production startup script for Django Doctor Appointment System

set -e

# Print environment info for debugging
echo "Environment variables:"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "DATABASE_URL: ${DATABASE_URL:0:20}..."
echo "SECRET_KEY: ${SECRET_KEY:0:10}..."

echo "Starting Django Doctor Appointment System..."

# Wait for database to be ready (Azure PostgreSQL)
echo "Waiting for database connection..."
python -c "
import os
import sys
import time
from urllib.parse import urlparse

try:
    import psycopg2
except ImportError:
    print('psycopg2 not available, skipping database check')
    sys.exit(0)

database_url = os.environ.get('DATABASE_URL')
if database_url:
    parsed = urlparse(database_url)
    for i in range(10):
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:],
                connect_timeout=10
            )
            conn.close()
            print('Database connection successful!')
            break
        except Exception as e:
            print(f'Database connection attempt {i+1}/10 failed: {e}')
            time.sleep(3)
    else:
        print('Database connection failed, but continuing...')
else:
    print('No DATABASE_URL provided, skipping database check')
"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput || echo "Migration failed, continuing..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || echo "Static files collection failed, continuing..."

# Create superuser if it doesn't exist (only in development)
if [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "Creating superuser if needed..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
END
fi

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --keep-alive 2 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    doctor_appointment.wsgi:application
