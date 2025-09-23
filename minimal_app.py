#!/usr/bin/env python3
"""
Ultra-minimal Django application for deployment testing
"""
import os
import sys
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path

# Configure Django settings
settings.configure(
    DEBUG=True,
    SECRET_KEY='minimal-secret-key-for-testing',
    ALLOWED_HOSTS=['*'],
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
)

def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Django Doctor Appointment System</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                font-family: Arial, sans-serif; 
                margin: 0; 
                padding: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 10px; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                text-align: center;
                max-width: 600px;
            }
            h1 { 
                color: #333; 
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .success { 
                color: #28a745; 
                font-size: 1.2em;
                margin: 20px 0;
            }
            .info { 
                background: #f8f9fa; 
                padding: 20px; 
                border-radius: 5px;
                margin: 20px 0;
            }
            .btn {
                display: inline-block;
                padding: 12px 24px;
                margin: 10px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                transition: background 0.3s;
            }
            .btn:hover {
                background: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Django Doctor Appointment System</h1>
            <div class="success">✅ Deployment Successful!</div>
            <div class="info">
                <p><strong>Your Django application is now running on Azure!</strong></p>
                <p>This is a minimal Django application demonstrating successful deployment.</p>
                <p><strong>Server:</strong> Azure Web App</p>
                <p><strong>Framework:</strong> Django</p>
                <p><strong>Status:</strong> Online</p>
            </div>
            <div>
                <a href="/admin/" class="btn">Admin Panel</a>
                <a href="https://github.com/joiceantony27/django-doctor-appointment" class="btn">GitHub Repository</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def health(request):
    return HttpResponse("OK", content_type="text/plain")

# URL patterns
urlpatterns = [
    path('', home, name='home'),
    path('health/', health, name='health'),
]

# WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
