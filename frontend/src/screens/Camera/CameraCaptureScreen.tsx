import React, { useEffect, useState, useCallback } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  ActivityIndicator,
  SafeAreaView,
  StatusBar,
} from "react-native";
import {
  Camera,
  useCameraDevice,
  useCameraPermission,
} from "react-native-vision-camera";
import { TelemetrySocketService } from "../../services/telemetrySocket";
import { UserSession } from "../../types/auth.types";
import { styles } from "./CameraCaptureScreen.styles";

interface CameraCaptureScreenProps {
  userSession?: UserSession | null;
  onLogout?: () => void;
}

export const CameraCaptureScreen: React.FC<CameraCaptureScreenProps> = ({
  userSession,
  onLogout,
}) => {
  const { hasPermission, requestPermission } = useCameraPermission();
  const device = useCameraDevice("back");

  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [feedback, setFeedback] = useState<string>(
    "Presiona 'Iniciar Análisis' para transmitir telemetría"
  );
  const [currentAngle, setCurrentAngle] = useState<number | null>(null);
  const [hasRiskAlert, setHasRiskAlert] = useState<boolean>(false);

  useEffect(() => {
    if (!hasPermission) {
      requestPermission();
    }
  }, [hasPermission, requestPermission]);

  const toggleAnalysis = useCallback(() => {
    if (isAnalyzing) {
      TelemetrySocketService.disconnect();
      setIsAnalyzing(false);
      setFeedback("Análisis detenido.");
      setCurrentAngle(null);
      setHasRiskAlert(false);
    } else {
      TelemetrySocketService.connect({
        onOpen: () => {
          setIsAnalyzing(true);
          setFeedback("Conectado. Transmitiendo telemetría en streaming...");
        },
        onFeedback: (res) => {
          if (res?.data) {
            setCurrentAngle(res.data.angulo_grados);
            setHasRiskAlert(Boolean(res.data.alerta_riesgo_lesion));
            setFeedback(
              `Ángulo: ${res.data.angulo_grados}° | ${res.data.diagnostico_tecnico}`
            );
          }
        },
        onError: (err) => {
          setFeedback(`Error en streaming: ${err}`);
          setIsAnalyzing(false);
        },
        onClose: () => setIsAnalyzing(false),
      });
    }
  }, [isAnalyzing]);

  if (!hasPermission) {
    return (
      <SafeAreaView style={styles.centerContainer}>
        <StatusBar barStyle="light-content" />
        <Text style={styles.titleText}>Permiso Requerido</Text>
        <Text style={styles.descriptionText}>
          BioMecanicSport necesita acceso a la cámara para realizar el análisis cinemático en tiempo real.
        </Text>
        <TouchableOpacity style={styles.primaryButton} onPress={requestPermission}>
          <Text style={styles.buttonText}>Conceder Permiso</Text>
        </TouchableOpacity>
      </SafeAreaView>
    );
  }

  if (!device) {
    return (
      <SafeAreaView style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#00E5FF" />
        <Text style={styles.descriptionText}>Inicializando sensor de cámara...</Text>
      </SafeAreaView>
    );
  }

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" translucent backgroundColor="transparent" />
      <Camera style={StyleSheet.absoluteFill} device={device} isActive={true} />

      {/* HUD Superior */}
      <SafeAreaView style={styles.hudOverlayTop}>
        <View style={styles.headerBar}>
          <View style={styles.badgeContainer}>
            <View style={[styles.statusDot, isAnalyzing ? styles.dotActive : styles.dotIdle]} />
            <Text style={styles.badgeText}>
              {userSession ? `${userSession.username.toUpperCase()} (${userSession.rol})` : "STREAMING"}
            </Text>
          </View>
          {onLogout && (
            <TouchableOpacity style={styles.logoutButton} onPress={onLogout}>
              <Text style={styles.logoutText}>Cerrar Sesión</Text>
            </TouchableOpacity>
          )}
        </View>

        {currentAngle !== null && (
          <View style={[styles.angleCard, hasRiskAlert ? styles.cardAlert : styles.cardNormal]}>
            <Text style={styles.angleLabel}>ÁNGULO ARTICULAR</Text>
            <Text style={styles.angleValue}>{currentAngle}°</Text>
            {hasRiskAlert && <Text style={styles.alertText}>⚠️ RIESGO LESIVO DETECTADO</Text>}
          </View>
        )}

        <View style={styles.infoBanner}>
          <Text style={styles.infoBannerText} numberOfLines={2}>{feedback}</Text>
        </View>
      </SafeAreaView>

      {/* Control Inferior */}
      <SafeAreaView style={styles.hudOverlayBottom}>
        <TouchableOpacity
          style={[styles.actionButton, isAnalyzing ? styles.actionButtonActive : styles.actionButtonIdle]}
          onPress={toggleAnalysis}
          activeOpacity={0.8}
        >
          <Text style={styles.actionButtonText}>
            {isAnalyzing ? "Detener Análisis" : "Iniciar Análisis"}
          </Text>
        </TouchableOpacity>
      </SafeAreaView>
    </View>
  );
};

export default CameraCaptureScreen;
