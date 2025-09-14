# Django Doctor Appointment System - Docker Deployment

This guide explains how to deploy the Django Doctor Appointment System using Docker.

## Files Created

- `Dockerfile` - Development Docker configuration
- `Dockerfile.production` - Production Docker configuration with Gunicorn
- `docker-compose.yml` - Multi-container setup with PostgreSQL and Redis
- `.dockerignore` - Optimizes Docker build by excluding unnecessary files
- `start.sh` - Startup script for container initialization
- `doctor_appointment/settings_production.py` - Production settings

## Quick Start

### Development Mode

1. **Build and run the container:**
   ```bash
   docker build -t doctor-appointment .
   docker run -p 8000:8000 doctor-appointment
   ```

2. **Access the application:**
   - Open http://localhost:8000 in your browser

### Production Mode with Docker Compose

1. **Update environment variables in docker-compose.yml:**
   ```yaml
   environment:
     - SECRET_KEY=your-actual-secret-key
     - EMAIL_HOST_USER=your-email@gmail.com
     - EMAIL_HOST_PASSWORD=your-app-password
     - STRIPE_PUBLISHABLE_KEY=your-stripe-publishable-key
     - STRIPE_SECRET_KEY=your-stripe-secret-key
     - RAZORPAY_KEY_ID=your-razorpay-key-id
     - RAZORPAY_KEY_SECRET=your-razorpay-key-secret
   ```

2. **Start all services:**
   ```bash
   docker-compose up -d
   ```

3. **Access the application:**
   - Open http://localhost:8000 in your browser

## Features Included

### Templates and Static Files
- ✅ All templates from `appointments/templates/` and `appointments/templates/appointments/`
- ✅ Static files properly collected and served
- ✅ Media files (images, PDFs) properly handled

### Dependencies
- ✅ All Python packages from requirements.txt
- ✅ System dependencies (gcc, libpq-dev, curl)
- ✅ Image processing libraries for Pillow
- ✅ PostgreSQL support

### Security
- ✅ Non-root user execution
- ✅ Production security settings
- ✅ Environment variable configuration
- ✅ Health checks

### Database
- ✅ PostgreSQL database container
- ✅ Automatic migrations
- ✅ Data persistence with volumes

### Additional Services
- ✅ Redis for caching and channels
- ✅ Email configuration
- ✅ Payment gateway support (Stripe & Razorpay)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Debug mode | False |
| `DB_NAME` | Database name | doctor_appointment |
| `DB_USER` | Database user | postgres |
| `DB_PASSWORD` | Database password | password |
| `DB_HOST` | Database host | localhost |
| `DB_PORT` | Database port | 5432 |
| `EMAIL_HOST_USER` | Email username | Required |
| `EMAIL_HOST_PASSWORD` | Email password | Required |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key | Required |
| `STRIPE_SECRET_KEY` | Stripe secret key | Required |
| `RAZORPAY_KEY_ID` | Razorpay key ID | Required |
| `RAZORPAY_KEY_SECRET` | Razorpay key secret | Required |

## Commands

### Build and Run
```bash
# Development
docker build -t doctor-appointment .
docker run -p 8000:8000 doctor-appointment

# Production with compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Database Operations
```bash
# Access database
docker-compose exec db psql -U postgres -d doctor_appointment

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Run migrations
docker-compose exec web python manage.py migrate
```

### Maintenance
```bash
# Update containers
docker-compose pull
docker-compose up -d

# Backup database
docker-compose exec db pg_dump -U postgres doctor_appointment > backup.sql

# Restore database
docker-compose exec -T db psql -U postgres doctor_appointment < backup.sql
```

## Troubleshooting

### Common Issues

1. **Port already in use:**
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"  # Use port 8001 instead
   ```

2. **Database connection issues:**
   ```bash
   # Check if database is running
   docker-compose ps
   
   # View database logs
   docker-compose logs db
   ```

3. **Static files not loading:**
   ```bash
   # Rebuild with static files
   docker-compose exec web python manage.py collectstatic --noinput
   ```

4. **Permission issues:**
   ```bash
   # Fix file permissions
   sudo chown -R $USER:$USER .
   ```

### Logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs web
docker-compose logs db
docker-compose logs redis
```

## Production Deployment

For production deployment:

1. Use `Dockerfile.production` instead of `Dockerfile`
2. Set up proper environment variables
3. Use a reverse proxy (nginx) for static files
4. Set up SSL certificates
5. Configure proper logging
6. Set up monitoring and backups

## Support

If you encounter any issues, check the logs and ensure all environment variables are properly set.
