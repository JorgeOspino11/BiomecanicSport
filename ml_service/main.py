"""
Punto de acceso raíz para el servidor ASGI (Uvicorn).
Reenvía la instancia de FastAPI configurada en la capa de infraestructura.
"""
from infrastructure.main import app

__all__ = ["app"]
