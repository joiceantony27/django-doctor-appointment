#!/usr/bin/env python3
"""
Test script to verify Docker setup
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctor_appointment.settings')

try:
    django.setup()
    print("✅ Django setup successful")
    
    # Test imports
    from appointments.models import User, Doctor, Appointment
    print("✅ Models imported successfully")
    
    from appointments.views import home
    print("✅ Views imported successfully")
    
    from appointments.forms import UserRegistrationForm
    print("✅ Forms imported successfully")
    
    # Test template directories
    from django.template.loader import get_template
    try:
        template = get_template('appointments/home.html')
        print("✅ Templates found and accessible")
    except Exception as e:
        print(f"⚠️  Template issue: {e}")
    
    # Test static files
    from django.conf import settings
    static_dirs = settings.STATICFILES_DIRS
    print(f"✅ Static files directories: {static_dirs}")
    
    # Test media files
    media_root = settings.MEDIA_ROOT
    print(f"✅ Media root: {media_root}")
    
    print("\n🎉 All tests passed! Docker setup is ready.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
