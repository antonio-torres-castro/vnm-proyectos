/**
 * Gestor seguro de tokens JWT
 * Maneja el almacenamiento, recuperación y validación de tokens
 */

const TOKEN_KEY = 'vnm_auth_token';
const USER_KEY = 'vnm_user_data';

/**
 * Guarda el token de forma segura
 * @param {string} token - Token JWT
 */
export const saveToken = (token) => {
  if (!token) {
    console.warn('Intento de guardar token vacío');
    return;
  }
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Recupera el token almacenado
 * @returns {string|null} Token JWT o null si no existe
 */
export const getToken = () => {
  try {
    return localStorage.getItem(TOKEN_KEY);
  } catch (error) {
    console.error('Error al recuperar token:', error);
    return null;
  }
};

/**
 * Elimina el token del almacenamiento
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
};

/**
 * Guarda los datos del usuario
 * @param {Object} userData - Datos del usuario
 */
export const saveUserData = (userData) => {
  if (!userData) return;
  localStorage.setItem(USER_KEY, JSON.stringify(userData));
};

/**
 * Recupera los datos del usuario
 * @returns {Object|null} Datos del usuario o null
 */
export const getUserData = () => {
  try {
    const userData = localStorage.getItem(USER_KEY);
    return userData ? JSON.parse(userData) : null;
  } catch (error) {
    console.error('Error al recuperar datos del usuario:', error);
    return null;
  }
};

/**
 * Verifica si el token existe y no está expirado
 * @returns {boolean} True si el token es válido
 */
export const isTokenValid = () => {
  const token = getToken();
  if (!token) return false;

  try {
    // Decodificar el payload del JWT (sin verificar la firma)
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split('')
        .map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
        .join('')
    );

    const decoded = JSON.parse(jsonPayload);
    const currentTime = Date.now() / 1000;

    // Verificar si el token no ha expirado
    return decoded.exp && decoded.exp > currentTime;
  } catch (error) {
    console.error('Error al validar token:', error);
    return false;
  }
};

/**
 * Obtiene los headers de autorización para las peticiones
 * @returns {Object} Headers con el token
 */
export const getAuthHeaders = () => {
  const token = getToken();
  return token 
    ? { Authorization: `Bearer ${token}` }
    : {};
};

/**
 * Limpia toda la información de autenticación
 */
export const clearAuthData = () => {
  removeToken();
  console.log('Datos de autenticación limpiados');
};
