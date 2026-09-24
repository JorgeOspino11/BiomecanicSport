import {
  KinematicFeedbackPayload,
  TelemetrySocketCallbacks,
} from "../types/telemetry.types";

/**
 * Servicio de Telemetría por WebSockets para BioMecanicSport.
 * Conecta la aplicación móvil con el Telemetry Server (Node/TS).
 */
export class TelemetrySocketService {
  private static socket: WebSocket | null = null;
  private static serverUrl: string = "ws://localhost:3000";

  public static setServerUrl(url: string): void {
    this.serverUrl = url;
  }

  public static connect(callbacks: TelemetrySocketCallbacks = {}): WebSocket {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      console.warn("[TelemetrySocket] Ya existe una conexión activa.");
      return this.socket;
    }

    console.log(`[TelemetrySocket] Conectando a ${this.serverUrl}...`);
    this.socket = new WebSocket(this.serverUrl);

    this.socket.onopen = () => {
      console.log("[TelemetrySocket] Conexión establecida.");
      callbacks.onOpen?.();
    };

    this.socket.onmessage = (event: WebSocketMessageEvent) => {
      try {
        const payload: KinematicFeedbackPayload = JSON.parse(
          event.data as string
        );
        if (payload.type === "KINEMATIC_FEEDBACK") {
          callbacks.onFeedback?.(payload);
        }
      } catch (err) {
        console.error("[TelemetrySocket] Error parseando payload:", err);
      }
    };

    this.socket.onerror = (event: any) => {
      const msg = event?.message || "Error en conexión WebSocket";
      console.error("[TelemetrySocket] Error en socket:", msg);
      callbacks.onError?.(msg);
    };

    this.socket.onclose = () => {
      console.log("[TelemetrySocket] Conexión cerrada.");
      this.socket = null;
      callbacks.onClose?.();
    };

    return this.socket;
  }

  public static sendFrame(frameData: ArrayBuffer | Blob): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(frameData);
    } else {
      console.warn("[TelemetrySocket] Socket no conectado para enviar frames.");
    }
  }

  public static disconnect(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  public static isConnected(): boolean {
    return this.socket !== null && this.socket.readyState === WebSocket.OPEN;
  }
}

export default TelemetrySocketService;
