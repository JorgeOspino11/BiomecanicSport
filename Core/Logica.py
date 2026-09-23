import cv2
import os
import json
from Modelos.modelos_datos import CameraConfigModel, PerfilAtletaModel, DiagnosticModel, crear_directorio_atleta
from Servicios.Graficador import GraficadorBiomecanico

class VideoProcessor:
    """Procesador de vídeo con OpenCV."""
    def __init__(self, camera_index: int = 0):
        self.camera_index = camera_index
        self.cap = None
        self.config = CameraConfigModel()

    def iniciar_camara(self) -> bool:
        self.cap = cv2.VideoCapture(self.camera_index)
        return self.cap.isOpened()

    def obtener_frame_procesado(self):
        if not self.cap or not self.cap.isOpened():
            return None, False

        ret, frame = self.cap.read()
        if not ret:
            return None, False

        if self.config.espejo:
            frame = cv2.flip(frame, 1)
        if self.config.escala_grises:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.config.negativo:
            frame = cv2.bitwise_not(frame)

        if self.config.mostrar_info:
            alto, ancho = frame.shape[:2]
            cx, cy = ancho // 2, alto // 2
            color = (0, 255, 0) if len(frame.shape) == 3 else 255
            cv2.line(frame, (cx - 15, cy), (cx + 15, cy), color, 2)
            cv2.line(frame, (cx, cy - 15), (cx, cy + 15), color, 2)
            cv2.putText(frame, f"Visor Biomecanico | {ancho}x{alto}", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        return frame, True

    def liberar_camara(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
            cv2.destroyAllWindows()


class BiomechanicalAnalyzer:
    """Módulo para procesar diagnósticos y generar reportes y gráficas."""
    @staticmethod
    def procesar_atleta_completo(atleta: PerfilAtletaModel) -> tuple[str, str]:
        # 1. Crear carpeta del deportista
        ruta_carpeta = crear_directorio_atleta(atleta)
        
        # 2. Diagnóstico simulado
        diagnostico = DiagnosticModel(
            angulo_promedio_rodilla=135.5,
            asimetria_porcentaje=4.2,
            frecuencia_cardiaca_estimada=142,
            alerta_lesion_valgo=False,
            nivel_fatiga="Moderado",
            observaciones_tecnicas=[
                "Alineación adecuada de cadera en extensión.",
                "Asimetría de apoyos del 4.2% detectada en aceleración.",
                "Patrón respiratorio estable durante la prueba."
            ]
        )

        # 3. Guardar datos en formato JSON
        archivo_json = os.path.join(ruta_carpeta, "diagnostico_tecnico.json")
        with open(archivo_json, "w", encoding="utf-8") as f:
            f.write(diagnostico.model_dump_json(indent=4))

        # 4. Guardar Documento Técnico en TXT
        archivo_txt = os.path.join(ruta_carpeta, "Reporte_Biomecanico.txt")
        with open(archivo_txt, "w", encoding="utf-8") as f:
            f.write("=== INFORME BIOMECÁNICO DE RENDIMIENTO ===\n")
            f.write(f"Atleta: {atleta.nombre} {atleta.apellido}\n")
            f.write(f"Deporte: {atleta.deporte} | Posición/Rol: {atleta.posicion_rol}\n")
            f.write(f"Edad: {atleta.edad} años | Peso: {atleta.peso_kg}kg | Altura: {atleta.altura_cm}cm\n")
            f.write("-------------------------------------------\n")
            f.write(f"Ángulo Articular Promedio: {diagnostico.angulo_promedio_rodilla}°\n")
            f.write(f"Asimetría Biomecánica: {diagnostico.asimetria_porcentaje}%\n")
            f.write(f"Frecuencia Cardíaca Estimada: {diagnostico.frecuencia_cardiaca_estimada} BPM\n")
            f.write(f"Alerta de Valgo de Rodilla: {'SÍ' if diagnostico.alerta_lesion_valgo else 'NO'}\n")
            f.write(f"Nivel de Fatiga: {diagnostico.nivel_fatiga}\n\n")
            f.write("Observaciones Técnicas:\n")
            for obs in diagnostico.observaciones_tecnicas:
                f.write(f" - {obs}\n")

        # 5. Generar y guardar la gráfica
        nombre_completo = f"{atleta.nombre} {atleta.apellido}"
        ruta_grafica = GraficadorBiomecanico.generar_grafico_rendimiento(ruta_carpeta, nombre_completo)

        return ruta_carpeta, ruta_grafica