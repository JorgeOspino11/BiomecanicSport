"""
Adaptador de Entrada (Driving Adapter): Routers HTTP con FastAPI.
Recibe peticiones web, valida esquemas con Pydantic y delega al Caso de Uso.
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from application.video_use_case import ProcesarVideoMovimientoUseCase

router = APIRouter(prefix="/analisis", tags=["Análisis Biomecánico"])


# Esquemas DTO (Data Transfer Objects) para la capa de presentación
class CoordenadaDTO(BaseModel):
    """Representación de un punto articular en el plano/espacio."""
    x: float = Field(..., description="Posición en eje X (píxeles o normalizada)")
    y: float = Field(..., description="Posición en eje Y (píxeles o normalizada)")
    z: Optional[float] = Field(default=0.0, description="Profundidad estimada en eje Z")


class SolicitudCalculoAnguloDTO(BaseModel):
    """Datos necesarios para calcular el ángulo articular."""
    nombre_articulacion: str = Field(default="Rodilla Derecha", description="Nombre del complejo articular")
    punto_origen: CoordenadaDTO = Field(..., description="Punto A (ej. Cadera)")
    vertice: CoordenadaDTO = Field(..., description="Punto B Vértice (ej. Rodilla)")
    punto_destino: CoordenadaDTO = Field(..., description="Punto C (ej. Tobillo)")


class RespuestaAnalisisDTO(BaseModel):
    """Respuesta serializada con el diagnóstico cinemático."""
    articulacion: str
    angulo_grados: float
    alerta_riesgo_lesion: bool
    diagnostico_tecnico: str
    timestamp: str


@router.post(
    "/angulo",
    response_model=RespuestaAnalisisDTO,
    status_code=status.HTTP_200_OK,
    summary="Calcular ángulo articular",
    description="Calcula el ángulo biomecánico entre tres coordenadas y evalúa el riesgo lesivo."
)
def calcular_angulo(solicitud: SolicitudCalculoAnguloDTO):
    try:
        # Instancia e invocación del caso de uso de aplicación
        caso_de_uso = ProcesarVideoMovimientoUseCase()
        resultado = caso_de_uso.ejecutar(
            punto_origen=solicitud.punto_origen.model_dump(),
            vertice_articular=solicitud.vertice.model_dump(),
            punto_destino=solicitud.punto_destino.model_dump(),
            nombre_articulacion=solicitud.nombre_articulacion
        )
        return resultado
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el procesamiento cinemático: {str(exc)}"
        )


@router.get(
    "/simulacion",
    response_model=RespuestaAnalisisDTO,
    summary="Ejecutar análisis biomecánico simulado",
    description="Endpoint demostrativo con coordenadas de Cadera, Rodilla y Tobillo preestablecidas."
)
def simulacion_movimiento():
    """Simula una flexión de rodilla típica en sentadilla o salto."""
    caso_de_uso = ProcesarVideoMovimientoUseCase()
    # Simulación: Cadera (100, 200), Rodilla (100, 300), Tobillo (180, 300) -> Forma un ángulo recto ~90°
    resultado = caso_de_uso.ejecutar(
        punto_origen={"x": 100.0, "y": 200.0, "z": 0.0},
        vertice_articular={"x": 100.0, "y": 300.0, "z": 0.0},
        punto_destino={"x": 180.0, "y": 300.0, "z": 0.0},
        nombre_articulacion="Rodilla en Sentadilla (Prueba)"
    )
    return resultado
