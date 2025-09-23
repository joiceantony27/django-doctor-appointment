#!/usr/bin/env python3
"""
Minimal Django app specifically for Azure Web App deployment
"""
import os
import sys
import django
from django.conf import settings
from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse
from django.urls import path

# Configure Django settings for Azure
settings.configure(
    DEBUG=False,
    SECRET_KEY=os.environ.get('SECRET_KEY', 'azure-deployment-secret-key-2024'),
    ALLOWED_HOSTS=['django-doctor-appointment.azurewebsites.net', 'localhost', '127.0.0.1', '*'],
    ROOT_URLCONF=__name__,
    MIDDLEWARE=[
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
    ],
    INSTALLED_APPS=[
        'django.contrib.staticfiles',
    ],
    STATIC_URL='/static/',
    STATIC_ROOT='/tmp/staticfiles',
)

django.setup()

def home(request):
    """Home page view"""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Django Doctor Appointment System - Live on Azure</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #333;
            }
            .container { 
                background: white;
                padding: 3rem;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 700px;
                width: 90%;
            }
            h1 { 
                color: #2c3e50;
                margin-bottom: 1rem;
                font-size: 2.5rem;
                font-weight: 700;
            }
            .success { 
                color: #27ae60;
                font-size: 1.3rem;
                margin: 1.5rem 0;
                font-weight: 600;
            }
            .info { 
                background: #f8f9fa;
                padding: 2rem;
                border-radius: 15px;
                margin: 2rem 0;
                border-left: 5px solid #3498db;
            }
            .feature-list {
                text-align: left;
                margin: 1rem 0;
            }
            .feature-list li {
                margin: 0.5rem 0;
                padding-left: 1rem;
            }
            .btn {
                display: inline-block;
                padding: 12px 30px;
                margin: 10px;
                background: #3498db;
                color: white;
                text-decoration: none;
                border-radius: 25px;
                transition: all 0.3s ease;
                font-weight: 600;
            }
            .btn:hover {
                background: #2980b9;
                transform: translateY(-2px);
            }
            .status {
                display: inline-block;
                padding: 8px 16px;
                background: #27ae60;
                color: white;
                border-radius: 20px;
                font-size: 0.9rem;
                margin: 0.5rem;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏥 Django Doctor Appointment System</h1>
            <div class="success">🎉 Successfully Deployed to Microsoft Azure!</div>
            
            <div class="info">
                <h3>🚀 Deployment Status</h3>
                <p><span class="status">✅ LIVE</span> <span class="status">✅ ONLINE</span> <span class="status">✅ ACCESSIBLE</span></p>
                
                <h4 style="margin-top: 1.5rem;">📊 Technical Details:</h4>
                <ul class="feature-list">
                    <li><strong>Platform:</strong> Microsoft Azure Web App</li>
                    <li><strong>Framework:</strong> Django 4.2.7</li>
                    <li><strong>Server:</strong> Gunicorn WSGI</li>
                    <li><strong>Container:</strong> Docker with Python 3.11</li>
                    <li><strong>CI/CD:</strong> GitHub Actions</li>
                    <li><strong>URL:</strong> https://django-doctor-appointment.azurewebsites.net</li>
                </ul>
                
                <h4 style="margin-top: 1.5rem;">🏗️ Infrastructure Ready:</h4>
                <ul class="feature-list">
                    <li>✅ Azure Resource Group (doctor-app-rg)</li>
                    <li>✅ Container Registry (doctorappregistry)</li>
                    <li>✅ PostgreSQL Database (doctor-app-db)</li>
                    <li>✅ GitHub Repository & Secrets</li>
                    <li>✅ Automated Deployment Pipeline</li>
                </ul>
            </div>
            
            <div>
                <a href="https://github.com/joiceantony27/django-doctor-appointment" class="btn">📂 View Source Code</a>
                <a href="/health/" class="btn">🔍 Health Check</a>
            </div>
            
            <p style="margin-top: 2rem; color: #7f8c8d; font-size: 0.9rem;">
                Deployment completed successfully. Ready for production features!
            </p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

def health(request):
    """Health check endpoint"""
    return HttpResponse("OK - Django Doctor Appointment System is running on Azure", content_type="text/plain")

def admin_redirect(request):
    """Admin redirect"""
    return HttpResponse("Admin panel will be available after full Django setup", content_type="text/plain")

# URL patterns
urlpatterns = [
    path('', home, name='home'),
    path('health/', health, name='health'),
    path('admin/', admin_redirect, name='admin'),
]

# WSGI application
application = get_wsgi_application()

if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
