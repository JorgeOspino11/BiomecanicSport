"""
Capa de Servicios (Service Layer) para la lógica de negocio de Atletas.
Aísla las reglas de negocio, validaciones y orquestación de la capa de vistas/controladores.
"""
import logging
from typing import Dict, Any, List
from django.core.exceptions import ValidationError
from .models import Atleta

logger = logging.getLogger(__name__)


class AtletaService:
    """
    Servicio que encapsula la lógica de negocio asociada a los atletas.
    """

    @staticmethod
    def validar_datos_antropometricos(datos: Dict[str, Any]) -> None:
        """
        Valida que las medidas físicas se encuentren en rangos fisiológicos coherentes.
        """
        peso = float(datos.get('peso_kg', 0))
        altura = float(datos.get('altura_cm', 0))
        edad = int(datos.get('edad', 0))

        if peso <= 20 or peso >= 300:
            raise ValidationError("El peso corporal debe estar entre 20 kg y 300 kg.")
        if altura <= 50 or altura >= 260:
            raise ValidationError("La estatura debe estar entre 50 cm y 260 cm.")
        if edad <= 3 or edad >= 120:
            raise ValidationError("La edad registrada no es válida para la prueba.")

    @classmethod
    def normalizar_datos(cls, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Limpia y estandariza los datos de entrada antes de persistir.
        """
        datos_limpios = datos.copy()
        if 'nombre' in datos_limpios and isinstance(datos_limpios['nombre'], str):
            datos_limpios['nombre'] = datos_limpios['nombre'].strip().title()
        if 'apellido' in datos_limpios and isinstance(datos_limpios['apellido'], str):
            datos_limpios['apellido'] = datos_limpios['apellido'].strip().title()
        if 'deporte' in datos_limpios and isinstance(datos_limpios['deporte'], str):
            datos_limpios['deporte'] = datos_limpios['deporte'].strip().title()
        return datos_limpios

    @classmethod
    def crear_perfil(cls, datos: Dict[str, Any]) -> Atleta:
        """
        Maneja la creación y registro de un nuevo perfil de atleta.
        Aplica validaciones de negocio, normaliza datos y persiste en base de datos.
        """
        logger.info(f"Iniciando creación de perfil para atleta: {datos.get('nombre')} {datos.get('apellido')}")
        
        # 1. Validación de reglas de negocio
        cls.validar_datos_antropometricos(datos)

        # 2. Normalización de formato
        datos_procesados = cls.normalizar_datos(datos)

        # 3. Persistencia mediante el ORM
        atleta = Atleta.objects.create(**datos_procesados)

        logger.info(f"Atleta creado con éxito. ID asignado: {atleta.id}")
        return atleta

    @staticmethod
    def obtener_por_id(atleta_id: int) -> Atleta:
        """
        Recupera un atleta por su identificador primario.
        """
        return Atleta.objects.get(id=atleta_id)

    @staticmethod
    def listar_todos() -> List[Atleta]:
        """
        Lista todos los atletas registrados ordenados cronológicamente.
        """
        return list(Atleta.objects.all())
