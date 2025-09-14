"""
Health check views for the Django Doctor Appointment System
"""
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

def health_check(request):
    """
    Health check endpoint for load balancers and monitoring
    """
    try:
        # Check database connectivity
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            db_status = "healthy"
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        db_status = "unhealthy"

    # Check cache connectivity
    try:
        cache.set('health_check', 'ok', 10)
        cache_status = "healthy" if cache.get('health_check') == 'ok' else "unhealthy"
    except Exception as e:
        logger.error(f"Cache health check failed: {e}")
        cache_status = "unhealthy"

    # Overall health status
    overall_status = "healthy" if db_status == "healthy" and cache_status == "healthy" else "unhealthy"
    
    status_code = 200 if overall_status == "healthy" else 503
    
    response_data = {
        "status": overall_status,
        "database": db_status,
        "cache": cache_status,
        "service": "django-doctor-appointment"
    }
    
    return JsonResponse(response_data, status=status_code)

def readiness_check(request):
    """
    Readiness check endpoint for Kubernetes
    """
    try:
        # Check if migrations are up to date
        from django.core.management import execute_from_command_line
        from django.core.management.commands.migrate import Command as MigrateCommand
        
        # This is a simplified check - in production you might want more sophisticated checks
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({"status": "ready"}, status=200)
    except Exception as e:
        logger.error(f"Readiness check failed: {e}")
        return JsonResponse({"status": "not ready", "error": str(e)}, status=503)

def liveness_check(request):
    """
    Liveness check endpoint for Kubernetes
    """
    return JsonResponse({"status": "alive"}, status=200)
