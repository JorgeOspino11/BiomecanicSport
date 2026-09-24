"""
Capa de Aplicación: Caso de uso para el procesamiento biomecánico de video y movimiento.
Orquesta las operaciones entre adaptadores externos y el núcleo de dominio.
"""
from typing import Dict, Any
from datetime import datetime
from domain.biomechanics import PuntoArticular, CalculadorBiomecanico


class ProcesarVideoMovimientoUseCase:
    """
    Caso de uso responsable de coordinar el análisis cinemático de fotogramas o puntos articulares.
    """

    def __init__(self, calculador: CalculadorBiomecanico = None):
        self.calculador = calculador or CalculadorBiomecanico()

    def ejecutar(
        self,
        punto_origen: Dict[str, float],
        vertice_articular: Dict[str, float],
        punto_destino: Dict[str, float],
        nombre_articulacion: str = "Rodilla Derecha"
    ) -> Dict[str, Any]:
        """
        Orquesta el flujo:
        1. Transforma diccionarios DTO a objetos puros del dominio (PuntoArticular).
        2. Ejecuta el cálculo matemático puro en el dominio.
        3. Evalúa si el rango entra en parámetros de riesgo lesivo.
        4. Retorna el resultado estructurado para la infraestructura.
        """
        print(f"[Caso de Uso] Procesando análisis para articulación: {nombre_articulacion}")

        # 1. Transformación a Entidades de Dominio
        p_a = PuntoArticular(
            x=punto_origen.get('x', 0.0),
            y=punto_origen.get('y', 0.0),
            z=punto_origen.get('z', 0.0)
        )
        p_vertice = PuntoArticular(
            x=vertice_articular.get('x', 0.0),
            y=vertice_articular.get('y', 0.0),
            z=vertice_articular.get('z', 0.0)
        )
        p_c = PuntoArticular(
            x=punto_destino.get('x', 0.0),
            y=punto_destino.get('y', 0.0),
            z=punto_destino.get('z', 0.0)
        )

        # 2. Invocación de reglas puras de dominio
        angulo_calculado = self.calculador.calcular_angulo_2d(p_a, p_vertice, p_c)
        alerta_riesgo = self.calculador.evaluar_alerta_movimiento(angulo_calculado)

        # 3. Diagnóstico deportivo derivado
        if alerta_riesgo:
            diagnostico = "Alerta: Ángulo articular fuera de rango seguro fisiológico."
        else:
            diagnostico = "Óptimo: Rango cinemático dentro de los estándares biomecánicos."

        print(f"[Caso de Uso] Resultado obtenido: {angulo_calculado}° | Alerta: {alerta_riesgo}")

        return {
            "articulacion": nombre_articulacion,
            "angulo_grados": angulo_calculado,
            "alerta_riesgo_lesion": alerta_riesgo,
            "diagnostico_tecnico": diagnostico,
            "timestamp": datetime.now().isoformat()
        }
