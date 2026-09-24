import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  StatusBar,
  SafeAreaView,
} from "react-native";
import { UserRole, UserSession } from "../../types/auth.types";
import { AuthService } from "../../services/authService";
import { styles } from "./LoginScreen.styles";

interface LoginScreenProps {
  onLoginSuccess: (session: UserSession) => void;
}

export const LoginScreen: React.FC<LoginScreenProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [rol, setRol] = useState<UserRole>("ATLETA");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleLogin = async () => {
    setErrorMessage(null);
    setIsLoading(true);

    try {
      const session = await AuthService.login({ username, password, rol });
      onLoginSuccess(session);
    } catch (err: any) {
      setErrorMessage(err.message || "Error al iniciar sesión.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="light-content" backgroundColor="#0A0E17" />
      <KeyboardAvoidingView
        behavior={Platform.OS === "ios" ? "padding" : "height"}
        style={styles.keyboardView}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          {/* Encabezado y Logo */}
          <View style={styles.headerContainer}>
            <View style={styles.logoBadge}>
              <Text style={styles.logoIconText}>⚡</Text>
            </View>
            <Text style={styles.title}>BioMecanicSport</Text>
            <Text style={styles.subtitle}>
              Plataforma de Telemetría y Cinemática
            </Text>
          </View>

          {/* Selector de Rol (Entrenador / Atleta) */}
          <View style={styles.roleSelectorContainer}>
            <TouchableOpacity
              style={[styles.roleTab, rol === "ATLETA" && styles.roleTabActive]}
              onPress={() => setRol("ATLETA")}
            >
              <Text
                style={[
                  styles.roleTabText,
                  rol === "ATLETA" && styles.roleTabTextActive,
                ]}
              >
                🏃 Atleta
              </Text>
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.roleTab,
                rol === "ENTRENADOR" && styles.roleTabActive,
              ]}
              onPress={() => setRol("ENTRENADOR")}
            >
              <Text
                style={[
                  styles.roleTabText,
                  rol === "ENTRENADOR" && styles.roleTabTextActive,
                ]}
              >
                📋 Entrenador
              </Text>
            </TouchableOpacity>
          </View>

          {/* Mensaje de Error */}
          {errorMessage && (
            <View style={styles.errorBox}>
              <Text style={styles.errorText}>{errorMessage}</Text>
            </View>
          )}

          {/* Formulario de Entrada */}
          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Usuario</Text>
            <TextInput
              style={styles.input}
              placeholder="Ingresa tu usuario (ej. nicolas)"
              placeholderTextColor="#484F58"
              value={username}
              onChangeText={setUsername}
              autoCapitalize="none"
            />
          </View>

          <View style={styles.inputGroup}>
            <Text style={styles.inputLabel}>Contraseña</Text>
            <TextInput
              style={styles.input}
              placeholder="••••••••"
              placeholderTextColor="#484F58"
              secureTextEntry
              value={password}
              onChangeText={setPassword}
            />
          </View>

          {/* Botón de Autenticación */}
          <TouchableOpacity
            style={[styles.submitButton, isLoading && styles.submitButtonDisabled]}
            onPress={handleLogin}
            disabled={isLoading}
            activeOpacity={0.85}
          >
            {isLoading ? (
              <ActivityIndicator color="#0A0E17" />
            ) : (
              <Text style={styles.submitButtonText}>Entrar a Telemetría</Text>
            )}
          </TouchableOpacity>

          <Text style={styles.footerText}>
            Conexión protegida con backend Django & WebSocket
          </Text>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

export default LoginScreen;
