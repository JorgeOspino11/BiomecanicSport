"""
Punto de Entrada de Infraestructura (FastAPI Application).
Configura middlewares, políticas de CORS y monta los adaptadores de entrada (routers).
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api.routers import router as biomecanica_router

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="BiomecanicSport - Microservicio de Machine Learning y Visión",
    description="Microservicio desarrollado bajo Arquitectura Hexagonal para análisis biomecánico y cinemático.",
    version="1.0.0",
)

# Configuración de políticas de CORS para comunicación con el Frontend y otros microservicios
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusión de adaptadores de entrada (Routers)
app.include_router(biomecanica_router)


@app.get("/", tags=["Información General"])
def inicio():
    """Ruta raíz con metadatos del servicio y su arquitectura."""
    return {
        "servicio": "BiomecanicSport ML Service",
        "arquitectura": "Hexagonal (Puertos y Adaptadores)",
        "estado": "en_linea",
        "servidor_redis": os.getenv("REDIS_HOST", "redis"),
        "documentacion_swagger": "/docs",
        "documentacion_redoc": "/redoc"
    }


@app.get("/health", tags=["Salud del Sistema"])
def verificacion_salud():
    """Endpoint de comprobación de salud para Docker / Kubernetes."""
    return {
        "estado": "saludable",
        "servicio": "ml_service"
    }
