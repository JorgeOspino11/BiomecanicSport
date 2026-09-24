/**
 * Tipos de datos para el módulo de Telemetría y Streaming cinemático.
 */
export interface KinematicData {
  status: string;
  session_id: string;
  frame_id: number;
  articulacion: string;
  angulo_grados: number;
  alerta_riesgo_lesion: boolean;
  diagnostico_tecnico: string;
  puntos_procesados: number;
  timestamp: string;
}

export interface KinematicFeedbackPayload {
  type: "KINEMATIC_FEEDBACK" | "ERROR" | "ACK";
  frame_id?: number;
  data?: KinematicData;
  error?: string;
  details?: string;
}

export interface TelemetrySocketCallbacks {
  onOpen?: () => void;
  onFeedback?: (feedback: KinematicFeedbackPayload) => void;
  onError?: (error: string) => void;
  onClose?: () => void;
}
