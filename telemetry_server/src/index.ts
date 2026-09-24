import http from "node:http";
import { WebSocketServer, WebSocket } from "ws";
import axios from "axios";

// Configuración de puertos y endpoints
const PORT = Number(process.env.TELEMETRY_PORT) || 3000;
const ML_SERVICE_URL =
  process.env.ML_SERVICE_URL || "http://ml_service:8001/analyze-telemetry";

// Servidor HTTP base para comprobación de salud (Health Check)
const server = http.createServer((req, res) => {
  if (req.url === "/health" && req.method === "GET") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(
      JSON.stringify({
        status: "healthy",
        service: "telemetry_server",
        timestamp: new Date().toISOString(),
      })
    );
    return;
  }

  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(
    JSON.stringify({
      name: "BioMecanicSport Telemetry Server",
      protocol: "WebSocket",
      ws_endpoint: `ws://localhost:${PORT}`,
      ml_target: ML_SERVICE_URL,
    })
  );
});

// Inicialización del Servidor WebSocket
const wss = new WebSocketServer({ server });

console.log(
  `[TelemetryServer] Iniciando servidor de streaming en puerto ${PORT}...`
);

wss.on("connection", (ws: WebSocket, req) => {
  const clientIp = req.socket.remoteAddress;
  console.log(`[TelemetryServer] Cliente conectado desde: ${clientIp}`);

  let frameCount = 0;

  ws.on("message", async (data: Buffer | ArrayBuffer | Buffer[], isBinary: boolean) => {
    frameCount++;

    try {
      if (isBinary) {
        const buffer = Buffer.isBuffer(data) ? data : Buffer.from(data as ArrayBuffer);
        console.log(
          `[TelemetryServer] Frame binario #${frameCount} recibido (${buffer.length} bytes). Desechando buffer de video en memoria...`
        );

        // =========================================================================
        // TODO: Run MediaPipe extraction here
        // 1. Decodificar frame o pasar buffer a MediaPipe Pose (@mediapipe/pose).
        // 2. Extraer puntos articulares normalizados (Keypoints: hombros, cadera, rodillas, tobillos).
        // 3. Descartar imagen/frame binario inmediatamente para evitar retención de memoria.
        // =========================================================================

        // Simulación de puntos articulares extraídos tras inferencia de MediaPipe Pose
        const simulatedTelemetryPayload = {
          session_id: `sess_stream_${Date.now()}`,
          frame_id: frameCount,
          timestamp: Date.now() / 1000,
          articulacion: "Rodilla Derecha",
          landmarks: [
            { name: "hip_right", x: 120.0 + Math.sin(frameCount) * 5, y: 200.0, z: 0.0, visibility: 0.99 },
            { name: "knee_right", x: 122.0, y: 310.0 + Math.cos(frameCount) * 10, z: 0.0, visibility: 0.98 },
            { name: "ankle_right", x: 190.0, y: 310.0, z: 0.0, visibility: 0.95 },
          ],
        };

        // Enviar coordenadas numéricas al microservicio de ML (FastAPI)
        console.log(
          `[TelemetryServer] Despachando coordenadas de telemetría a ${ML_SERVICE_URL}...`
        );
        const mlResponse = await axios.post(
          ML_SERVICE_URL,
          simulatedTelemetryPayload,
          {
            headers: { "Content-Type": "application/json" },
            timeout: 5000,
          }
        );

        console.log(
          `[TelemetryServer] Diagnóstico recibido de ML (Ángulo: ${mlResponse.data.angulo_grados}°, Alerta: ${mlResponse.data.alerta_riesgo_lesion})`
        );

        // Retransmitir resultado cinemático procesado al cliente en tiempo real
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(
            JSON.stringify({
              type: "KINEMATIC_FEEDBACK",
              frame_id: frameCount,
              data: mlResponse.data,
            })
          );
        }
      } else {
        // Mensaje de control o ping en formato texto
        const messageText = data.toString();
        console.log(`[TelemetryServer] Mensaje de texto/control recibido: ${messageText}`);

        ws.send(
          JSON.stringify({
            type: "ACK",
            message: "Control frame acknowledged",
          })
        );
      }
    } catch (error: any) {
      console.error(
        `[TelemetryServer] Error procesando frame #${frameCount}:`,
        error.message || error
      );

      if (ws.readyState === WebSocket.OPEN) {
        ws.send(
          JSON.stringify({
            type: "ERROR",
            error: "Error al procesar telemetría en ML",
            details: error.message,
          })
        );
      }
    }
  });

  ws.on("close", () => {
    console.log(`[TelemetryServer] Cliente desconectado (${clientIp}). Total frames procesados: ${frameCount}`);
  });

  ws.on("error", (err) => {
    console.error(`[TelemetryServer] Error en socket del cliente:`, err);
  });
});

server.listen(PORT, "0.0.0.0", () => {
  console.log(`[TelemetryServer] Servidor listo y escuchando en http://0.0.0.0:${PORT}`);
  console.log(`[TelemetryServer] WebSocket endpoint activo en ws://0.0.0.0:${PORT}`);
});
