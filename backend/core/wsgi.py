"""
Configuración WSGI para el proyecto core (BiomecanicSport).
Expone la variable invocable WSGI a nivel de módulo con el nombre 'application'.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
