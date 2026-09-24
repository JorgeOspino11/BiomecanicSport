import { LoginFormData, UserSession } from "../types/auth.types";

/**
 * Servicio encargado de gestionar la autenticación con el Backend Django.
 */
export class AuthService {
  /**
   * Valida credenciales e inicializa sesión para el atleta o entrenador.
   */
  public static async login(credentials: LoginFormData): Promise<UserSession> {
    const { username, password, rol } = credentials;

    // Validación Clean Code a nivel servicio
    if (!username.trim() || !password.trim()) {
      throw new Error("Debe ingresar un nombre de usuario y contraseña válidos.");
    }

    // Simulación de autenticación (fácilmente sustituible por fetch a /api/token/ o /api/login/)
    await new Promise((resolve) => setTimeout(resolve, 800));

    return {
      id: Math.floor(Math.random() * 1000) + 1,
      username: username.trim(),
      nombreCompleto: username.charAt(0).toUpperCase() + username.slice(1),
      email: `${username.toLowerCase()}@biomecanicsport.com`,
      rol,
      token: `bms_mock_jwt_token_${Date.now()}`,
    };
  }
}
