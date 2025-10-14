/**
 * Servicio de autenticación
 * Maneja todas las peticiones relacionadas con autenticación al backend
 */
import axios from 'axios';
import { 
  saveToken, 
  saveUserData, 
  getToken, 
  removeToken, 
  getAuthHeaders,
  clearAuthData 
} from '../utils/tokenManager';

// Configuración base de axios
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Instancia de axios configurada
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos
});

// Interceptor para agregar el token automáticamente
apiClient.interceptors.request.use(
  (config) => {
    const authHeaders = getAuthHeaders();
    config.headers = { ...config.headers, ...authHeaders };
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar respuestas y errores de autenticación
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      clearAuthData();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

/**
 * Realiza el login del usuario
 * @param {Object} credentials - Credenciales del usuario
 * @param {string} credentials.username - Nombre de usuario
 * @param {string} credentials.password - Contraseña
 * @returns {Promise<Object>} Datos del usuario y token
 */
export const login = async (credentials) => {
  try {
    console.log('Intentando login para:', credentials.username);
    
    // Preparar datos en formato JSON para el endpoint login-form
    const loginData = {
      email: credentials.username, // El backend espera 'email', no 'username'
      clave: credentials.password  // El backend espera 'clave', no 'password'
    };

    const response = await apiClient.post('/auth/login-form', loginData);

    const { access_token, token_type } = response.data;

    if (!access_token) {
      throw new Error('Token no recibido del servidor');
    }

    // Guardar token
    saveToken(access_token);
    
    console.log('Login exitoso para:', credentials.username);
    
    return {
      success: true,
      token: access_token,
      tokenType: token_type,
      user: null, // El usuario se obtendrá después con checkAuthStatus
      message: 'Login exitoso'
    };

  } catch (error) {
    console.error('Error en login:', error);
    
    let errorMessage = 'Error de conexión con el servidor';
    
    if (error.response) {
      // Error del servidor
      switch (error.response.status) {
        case 401:
          errorMessage = 'Credenciales incorrectas';
          break;
        case 422:
          errorMessage = 'Datos de login inválidos';
          break;
        case 500:
          errorMessage = 'Error interno del servidor';
          break;
        default:
          errorMessage = `Error del servidor: ${error.response.status}`;
      }
    } else if (error.request) {
      // Sin respuesta del servidor
      errorMessage = 'No se pudo conectar con el servidor';
    }

    return {
      success: false,
      message: errorMessage,
      error: error.response?.data?.detail || error.message
    };
  }
};

/**
 * Cierra la sesión del usuario
 * @returns {Promise<Object>} Resultado del logout
 */
export const logout = async () => {
  try {
    // Intentar hacer logout en el servidor
    await apiClient.post('/auth/logout');
    
    // Limpiar datos locales
    clearAuthData();
    
    console.log('Logout exitoso');
    return { success: true, message: 'Sesión cerrada correctamente' };
    
  } catch (error) {
    console.error('Error en logout:', error);
    
    // Aunque falle el logout en el servidor, limpiar datos locales
    clearAuthData();
    
    return { 
      success: true, // Siempre consideramos exitoso el logout local
      message: 'Sesión cerrada localmente' 
    };
  }
};

/**
 * Verifica si el usuario está autenticado
 * @returns {Promise<Object>} Estado de autenticación
 */
export const checkAuthStatus = async () => {
  try {
    const token = getToken();
    if (!token) {
      return { isAuthenticated: false, user: null };
    }

    // Verificar con el servidor que el token sigue siendo válido
    const response = await apiClient.get('/auth/me');
    
    if (response.data) {
      // Actualizar datos del usuario
      saveUserData(response.data);
      return { 
        isAuthenticated: true, 
        user: response.data 
      };
    }

    return { isAuthenticated: false, user: null };
    
  } catch (error) {
    console.error('Error verificando autenticación:', error);
    
    // Si hay error, limpiar tokens
    if (error.response?.status === 401) {
      clearAuthData();
    }
    
    return { isAuthenticated: false, user: null };
  }
};

/**
 * Obtiene el perfil del usuario actual
 * @returns {Promise<Object>} Datos del usuario
 */
export const getCurrentUser = async () => {
  try {
    const response = await apiClient.get('/auth/me');
    return {
      success: true,
      user: response.data
    };
  } catch (error) {
    console.error('Error obteniendo usuario actual:', error);
    return {
      success: false,
      message: 'Error al obtener datos del usuario',
      error: error.message
    };
  }
};

/**
 * Exporta la instancia configurada de axios para uso en otros servicios
 */
export { apiClient };

export default {
  login,
  logout,
  checkAuthStatus,
  getCurrentUser,
  apiClient
};
