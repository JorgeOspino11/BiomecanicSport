"""
Modelos de dominio y persistencia para la aplicación core_app.
"""
from django.db import models


class Atleta(models.Model):
    """
    Entidad de persistencia que almacena el perfil antropométrico y deportivo.
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    fecha_nacimiento = models.DateField(null=True, blank=True)
    peso_kg = models.DecimalField(max_digits=5, decimal_places=2, help_text="Peso en kilogramos")
    altura_cm = models.DecimalField(max_digits=5, decimal_places=2, help_text="Estatura en centímetros")
    deporte = models.CharField(max_length=100, default="Fútbol")
    posicion_rol = models.CharField(max_length=100, default="Atleta")
    dominancia = models.CharField(max_length=50, default="Derecho")
    lesiones_previas = models.TextField(blank=True, default="Ninguna")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'atletas'
        verbose_name = 'Atleta'
        verbose_name_plural = 'Atletas'
        ordering = ['-creado_en']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.deporte})"
