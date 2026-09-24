"""
Configuración de URLs del proyecto core (Backend BiomecanicSport).
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse


def verificacion_salud(request):
    """Endpoint para comprobaciones de estado (health check) del backend."""
    return JsonResponse({
        "estado": "saludable",
        "servicio": "backend",
        "aplicacion": "BiomecanicSport"
    })


urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    # Endpoint de verificación de estado
    path('api/health/', verificacion_salud, name='verificacion-salud'),
    # API de gestión deportiva
    path('api/', include('core_app.urls')),
]
