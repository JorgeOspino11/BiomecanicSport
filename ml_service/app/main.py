"""
Microservicio de Machine Learning y Procesamiento de Video (BiomecanicSport).
Desarrollado con FastAPI y OpenCV para análisis cinemático y biomecánico.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(
    title="BiomecanicSport ML & Video Processing Service",
    description="Microservicio de visión por computador y análisis biomecánico con OpenCV y modelos de estimación de pose.",
    version="1.0.0",
)

# Configuración de políticas de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def inicio():
    """Ruta raíz del microservicio con información básica de estado."""
    return {
        "servicio": "BiomecanicSport ML Service",
        "estado": "en_linea",
        "version": "1.0.0",
        "servidor_redis": os.getenv("REDIS_HOST", "redis"),
    }

@app.get("/health")
def verificacion_salud():
    """Endpoint de verificación de estado y salud del microservicio."""
    return {
        "estado": "saludable",
        "servicio": "ml_service"
    }
