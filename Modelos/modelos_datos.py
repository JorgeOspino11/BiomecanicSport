import os
from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from datetime import datetime

class CameraConfigModel(BaseModel):
    """Configuración del visor y procesamiento técnico."""
    espejo: bool = True
    escala_grises: bool = False
    negativo: bool = False
    mostrar_info: bool = True
    resolucion: Tuple[int, int] = (640, 480)

class ItemModel(BaseModel):
    """Modelo genérico para mantener compatibilidad."""
    id: Optional[int] = None
    nombre: str = "Registro Biomecánico"
    estado: bool = True

class PerfilAtletaModel(BaseModel):
    """Modelo con todos los datos antropométricos y deportivos del atleta."""
    nombre: str
    apellido: str
    edad: int
    fecha_nacimiento: str
    peso_kg: float
    altura_cm: float
    deporte: str
    posicion_rol: str
    dominancia: str = "Derecho"
    lesiones_previas: Optional[str] = "Ninguna"

class DiagnosticModel(BaseModel):
    """Modelo para registrar el análisis técnico calculado por visión por computador."""
    timestamp: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    angulo_promedio_rodilla: float
    asimetria_porcentaje: float
    frecuencia_cardiaca_estimada: int
    alerta_lesion_valgo: bool
    nivel_fatiga: str
    observaciones_tecnicas: List[str]

def crear_directorio_atleta(atleta: PerfilAtletaModel, base_dir: str = "Data/Deportistas") -> str:
    """Crea automáticamente la carpeta estructurada dentro del sistema para el deportista."""
    nombre_carpeta = f"{atleta.nombre}_{atleta.apellido}".replace(" ", "_").lower()
    ruta_atleta = os.path.join(base_dir, nombre_carpeta)
    os.makedirs(ruta_atleta, exist_ok=True)
    return ruta_atleta