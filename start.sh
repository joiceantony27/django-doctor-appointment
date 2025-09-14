#!/bin/bash

# Production startup script for Django Doctor Appointment System

set -e

echo "Starting Django Doctor Appointment System..."

# Wait for database to be ready (if using external database)
if [ -n "$DB_HOST" ]; then
    echo "Waiting for database..."
    while ! nc -z $DB_HOST $DB_PORT; do
        sleep 1
    done
    echo "Database is ready!"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

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
