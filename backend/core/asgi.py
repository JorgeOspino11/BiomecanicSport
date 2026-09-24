"""
Configuración ASGI para el proyecto core (BiomecanicSport).
Expone la variable invocable ASGI a nivel de módulo con el nombre 'application'.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_asgi_application()
