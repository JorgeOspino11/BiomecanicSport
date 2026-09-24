"""
Capa de Dominio: Entidades y Servicios de Dominio Biomecánico.
Contiene lógica matemática y física pura sin dependencias de frameworks web ni bases de datos.
"""
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PuntoArticular:
    """
    Entidad de dominio que representa las coordenadas espaciales de una articulación.
    """
    x: float
    y: float
    z: float = 0.0
    visibilidad: float = 1.0


class CalculadorBiomecanico:
    """
    Servicio de dominio para el cálculo cinemático y análisis articular.
    """

    @staticmethod
    def calcular_angulo_2d(
        punto_a: PuntoArticular,
        vertice: PuntoArticular,
        punto_c: PuntoArticular
    ) -> float:
        """
        Calcula el ángulo interior en grados formado en el vértice por los segmentos
        (punto_a -> vertice) y (punto_c -> vertice).
        Utiliza el arcotangente2 para garantizar estabilidad numérica.
        """
        # Vectores orientados desde el vértice hacia los extremos
        vector_ba = (punto_a.x - vertice.x, punto_a.y - vertice.y)
        vector_bc = (punto_c.x - vertice.x, punto_c.y - vertice.y)

        # Ángulos directores de cada segmento
        angulo_rad_ba = math.atan2(vector_ba[1], vector_ba[0])
        angulo_rad_bc = math.atan2(vector_bc[1], vector_bc[0])

        diferencia = abs(angulo_rad_ba - angulo_rad_bc)
        angulo_grados = math.degrees(diferencia)

        # Ajuste al ángulo convexo interior (0° a 180°)
        if angulo_grados > 180.0:
            angulo_grados = 360.0 - angulo_grados

        return round(angulo_grados, 2)

    @staticmethod
    def evaluar_alerta_movimiento(angulo: float, rango_minimo: float = 60.0, rango_maximo: float = 175.0) -> bool:
        """
        Determina si un ángulo se encuentra fuera de los umbrales seguros fisiológicos.
        Retorna True si hay alerta de sobreextensión o flexión anómala.
        """
        return bool(angulo < rango_minimo or angulo > rango_maximo)
