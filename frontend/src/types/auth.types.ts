/**
 * Tipos de datos para el módulo de Autenticación y Usuarios.
 */
export type UserRole = "ATLETA" | "ENTRENADOR";

export interface UserSession {
  id: number;
  username: string;
  nombreCompleto: string;
  email: string;
  rol: UserRole;
  token?: string;
}

export interface LoginFormData {
  username: string;
  password: string;
  rol: UserRole;
}
