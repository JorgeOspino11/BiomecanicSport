import React, { useState } from "react";
import { UserSession } from "./src/types/auth.types";
import { LoginScreen, CameraCaptureScreen } from "./src/screens";

/**
 * Componente Raíz de la Aplicación Móvil BioMecanicSport.
 * Orquesta la navegación basada en estado de autenticación.
 */
export default function App() {
  const [currentUser, setCurrentUser] = useState<UserSession | null>(null);

  const handleLoginSuccess = (session: UserSession) => {
    console.log(`[App] Sesión iniciada: ${session.username} (${session.rol})`);
    setCurrentUser(session);
  };

  const handleLogout = () => {
    console.log("[App] Cerrando sesión...");
    setCurrentUser(null);
  };

  if (!currentUser) {
    return <LoginScreen onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <CameraCaptureScreen
      userSession={currentUser}
      onLogout={handleLogout}
    />
  );
}
