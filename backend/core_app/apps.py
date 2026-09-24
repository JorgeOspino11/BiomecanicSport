"""Configuración de la aplicación core_app."""
from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_app'
    verbose_name = 'Núcleo de Gestión Deportiva'
