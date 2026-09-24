"""
Modelos de dominio y persistencia para la aplicación core_app.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    """
    Modelo de Usuario extendido para la plataforma BiomecanicSport.
    Permite autenticar usuarios y definir su rol dentro del ecosistema (Entrenador o Atleta).
    """
    class Rol(models.TextChoices):
        ENTRENADOR = "ENTRENADOR", "Entrenador"
        ATLETA = "ATLETA", "Atleta"

    rol = models.CharField(
        max_length=20,
        choices=Rol.choices,
        default=Rol.ATLETA,
        help_text="Rol del usuario en la plataforma (Entrenador o Atleta)"
    )

    class Meta:
        db_table = "usuarios"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"


class PerfilAtleta(models.Model):
    """
    Perfil biométrico y deportivo asociado 1 a 1 con un Usuario de rol Atleta.
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name="perfil_atleta",
        help_text="Cuenta de usuario asociada a este perfil"
    )
    peso_kg = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Peso en kilogramos"
    )
    altura_cm = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Estatura en centímetros"
    )
    deporte = models.CharField(
        max_length=100,
        default="Fútbol",
        help_text="Disciplina deportiva principal"
    )
    posicion = models.CharField(
        max_length=100,
        default="General",
        help_text="Posición de juego o especialidad biomecánica"
    )
    fecha_nacimiento = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha de nacimiento del atleta"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "perfiles_atletas"
        verbose_name = "Perfil de Atleta"
        verbose_name_plural = "Perfiles de Atletas"
        ordering = ["-creado_en"]

    def __str__(self):
        nombre_completo = self.usuario.get_full_name() or self.usuario.username
        return f"Perfil: {nombre_completo} ({self.deporte} - {self.posicion})"


class SesionEntrenamiento(models.Model):
    """
    Registro de una sesión de entrenamiento o evaluación biomecánica.
    Relación 1 a N con PerfilAtleta.
    """
    atleta = models.ForeignKey(
        PerfilAtleta,
        on_delete=models.CASCADE,
        related_name="sesiones",
        help_text="Atleta evaluado en la sesión"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        help_text="Fecha y hora de inicio de la sesión"
    )
    tipo_ejercicio = models.CharField(
        max_length=100,
        help_text="Tipo de ejercicio biomecánico (ej. Sentadilla, Sprint, Salto Vertical)"
    )
    angulo_maximo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Ángulo articular máximo alcanzado durante el movimiento (°)"
    )
    velocidad_media = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Velocidad media de ejecución estimada (m/s o °/s)"
    )
    weaviate_vector_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Identificador único del vector embebido de la serie en Weaviate"
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "sesiones_entrenamiento"
        verbose_name = "Sesión de Entrenamiento"
        verbose_name_plural = "Sesiones de Entrenamiento"
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.tipo_ejercicio} | {self.atleta.usuario.username} ({self.fecha.strftime('%Y-%m-%d %H:%M')})"


class Atleta(models.Model):
    """
    Entidad de persistencia que almacena el perfil antropométrico y deportivo (Legacy).
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
