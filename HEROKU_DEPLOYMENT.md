# Deploy Django Doctor Appointment System to Heroku

## Quick Deploy Button
[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/joiceantony27/django-doctor-appointment)

## Manual Deployment Steps

### 1. Install Heroku CLI
```bash
# Ubuntu/Debian
curl https://cli-assets.heroku.com/install.sh | sh

# macOS
brew tap heroku/brew && brew install heroku
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
heroku create django-doctor-appointment-live
```

### 4. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS="django-doctor-appointment-live.herokuapp.com"
```

### 5. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 6. Deploy Application
```bash
git push heroku main
```

### 7. Run Database Migrations
```bash
heroku run python manage.py migrate
heroku run python manage.py collectstatic --noinput
heroku run python manage.py createsuperuser
```

### 8. Open Application
```bash
heroku open
```

## Files Added for Heroku Deployment
- `Procfile` - Defines how to run the application
- `runtime.txt` - Specifies Python version
- `app.json` - Heroku app configuration
- Updated `settings.py` with database URL and whitenoise

## Environment Variables Required
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False for production
- `ALLOWED_HOSTS` - Your Heroku app domain
- `DATABASE_URL` - Automatically set by Heroku PostgreSQL addon

Your Django Doctor Appointment System will be live at:
https://django-doctor-appointment-live.herokuapp.com
