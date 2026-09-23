import matplotlib
matplotlib.use("Agg")  # Permite renderizar gráficos sin interfaz de Matplotlib
import matplotlib.pyplot as plt
import os
import numpy as np

class GraficadorBiomecanico:
    @staticmethod
    def generar_grafico_rendimiento(ruta_carpeta: str, nombre_atleta: str) -> str:
        """Genera y guarda una gráfica del comportamiento articular y fatiga acumulada."""
        tiempo = np.linspace(0, 10, 100)
        angulo_rodilla = 120 + 25 * np.sin(2 * np.pi * 0.5 * tiempo) + np.random.normal(0, 1.5, 100)
        fatiga_acumulada = np.linspace(15, 80, 100)

        fig, ax1 = plt.subplots(figsize=(7, 3.8))

        # Curva 1: Ángulo articular
        color_angulo = 'tab:blue'
        ax1.set_xlabel('Tiempo de Ejecución (s)')
        ax1.set_ylabel('Ángulo de Rodilla (°)', color=color_angulo)
        ax1.plot(tiempo, angulo_rodilla, color=color_angulo, linewidth=2, label="Ángulo Articular")
        ax1.tick_params(axis='y', labelcolor=color_angulo)
        ax1.grid(True, linestyle='--', alpha=0.5)

        # Curva 2: Estimación de Fatiga
        ax2 = ax1.twinx()
        color_fatiga = 'tab:red'
        ax2.set_ylabel('Índice de Fatiga (%)', color=color_fatiga)
        ax2.plot(tiempo, fatiga_acumulada, color=color_fatiga, linestyle=':', linewidth=2, label="Fatiga")
        ax2.tick_params(axis='y', labelcolor=color_fatiga)

        plt.title(f"Análisis Cinemático y Degradación Técnica - {nombre_atleta}")
        fig.tight_layout()

        # Guardar en la carpeta del deportista
        ruta_grafica = os.path.join(ruta_carpeta, "grafica_rendimiento.png")
        plt.savefig(ruta_grafica, dpi=150)
        plt.close(fig)
        return ruta_grafica