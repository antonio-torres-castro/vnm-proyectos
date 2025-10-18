/**
 * Contexto de Autenticación
 * Proporciona estado global de autenticación a toda la aplicación
 */
import React, { createContext, useContext, useReducer, useEffect, useCallback, useMemo } from 'react';
import { 
  login as apiLogin, 
  logout as apiLogout, 
  checkAuthStatus 
} from '../services/authService';
import { 
  getUserData, 
  isTokenValid, 
  clearAuthData 
} from '../utils/tokenManager';

// Estados posibles de autenticación
const AUTH_STATES = {
  LOADING: 'loading',
  AUTHENTICATED: 'authenticated',
  UNAUTHENTICATED: 'unauthenticated',
  ERROR: 'error'
};

// Acciones del reducer
const AUTH_ACTIONS = {
  LOADING: 'LOADING',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_ERROR: 'LOGIN_ERROR',
  LOGOUT: 'LOGOUT',
  UPDATE_USER: 'UPDATE_USER',
  SET_ERROR: 'SET_ERROR',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Estado inicial
const initialState = {
  status: AUTH_STATES.LOADING,
  user: null,
  isAuthenticated: false,
  error: null,
  isLoading: false
};

// Reducer para manejar las transiciones de estado
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.LOADING:
      return {
        ...state,
        isLoading: true,
        error: null
      };

    case AUTH_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        status: AUTH_STATES.AUTHENTICATED,
        user: action.payload.user,
        isAuthenticated: true,
        isLoading: false,
        error: null
      };

    case AUTH_ACTIONS.LOGIN_ERROR:
      return {
        ...state,
        status: AUTH_STATES.UNAUTHENTICATED,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload.error
      };

    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        status: AUTH_STATES.UNAUTHENTICATED,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null
      };

    case AUTH_ACTIONS.UPDATE_USER:
      return {
        ...state,
        user: action.payload.user
      };

    case AUTH_ACTIONS.SET_ERROR:
      return {
        ...state,
        error: action.payload.error,
        isLoading: false
      };

    case AUTH_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };

    default:
      return state;
  }
};

// Crear el contexto
const AuthContext = createContext();

/**
 * Proveedor del contexto de autenticación
 */
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Verificar autenticación al cargar la aplicación
  useEffect(() => {
    const initializeAuth = async () => {
      dispatch({ type: AUTH_ACTIONS.LOADING });

      try {
        // Verificar si hay token válido
        if (!isTokenValid()) {
          clearAuthData();
          dispatch({ type: AUTH_ACTIONS.LOGOUT });
          return;
        }

        // Verificar con el servidor
        const authStatus = await checkAuthStatus();
        
        if (authStatus.isAuthenticated && authStatus.user) {
          dispatch({ 
            type: AUTH_ACTIONS.LOGIN_SUCCESS, 
            payload: { user: authStatus.user } 
          });
        } else {
          clearAuthData();
          dispatch({ type: AUTH_ACTIONS.LOGOUT });
        }
      } catch (error) {
        console.error('Error inicializando autenticación:', error);
        clearAuthData();
        dispatch({ 
          type: AUTH_ACTIONS.LOGIN_ERROR, 
          payload: { error: 'Error de conexión' } 
        });
      }
    };

    initializeAuth();
  }, []);

  /**
   * Función de login
   */
  const login = useCallback(async (credentials) => {
    dispatch({ type: AUTH_ACTIONS.LOADING });
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });

    try {
      const result = await apiLogin(credentials);

      if (result.success) {
        dispatch({ 
          type: AUTH_ACTIONS.LOGIN_SUCCESS, 
          payload: { user: result.user } 
        });
        return { success: true, user: result.user };
      } else {
        dispatch({ 
          type: AUTH_ACTIONS.LOGIN_ERROR, 
          payload: { error: result.message } 
        });
        return { success: false, error: result.message };
      }
    } catch (error) {
      const errorMessage = 'Error inesperado durante el login';
      dispatch({ 
        type: AUTH_ACTIONS.LOGIN_ERROR, 
        payload: { error: errorMessage } 
      });
      return { success: false, error: errorMessage };
    }
  }, []);

  /**
   * Función de logout
   */
  const logout = useCallback(async () => {
    console.log('🔍 CONTEXT: logout iniciado');
    dispatch({ type: AUTH_ACTIONS.LOADING });

    try {
      console.log('🔍 CONTEXT: Llamando apiLogout...');
      await apiLogout();
      console.log('🔍 CONTEXT: apiLogout completado');
    } catch (error) {
      console.error('🔍 CONTEXT: Error en apiLogout:', error);
    } finally {
      console.log('🔍 CONTEXT: Limpiando datos y despachando LOGOUT');
      clearAuthData();
      dispatch({ type: AUTH_ACTIONS.LOGOUT });
    }
  }, []);

  /**
   * Actualizar datos del usuario
   */
  const updateUser = useCallback((userData) => {
    dispatch({ 
      type: AUTH_ACTIONS.UPDATE_USER, 
      payload: { user: userData } 
    });
  }, []);

  /**
   * Limpiar errores
   */
  const clearError = useCallback(() => {
    dispatch({ type: AUTH_ACTIONS.CLEAR_ERROR });
  }, []);

  /**
   * Establecer error
   */
  const setError = useCallback((error) => {
    dispatch({ 
      type: AUTH_ACTIONS.SET_ERROR, 
      payload: { error } 
    });
  }, []);

  // Valor del contexto memoizado
  const contextValue = useMemo(() => ({
    // Estado
    ...state,
    
    // Funciones
    login,
    logout,
    updateUser,
    clearError,
    setError,

    // Getters de conveniencia
    isLoggedIn: state.isAuthenticated,
    currentUser: state.user,
    authStatus: state.status
  }), [state, login, logout, updateUser, clearError, setError]);

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

/**
 * Hook para usar el contexto de autenticación
 */
export const useAuthContext = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuthContext debe ser usado dentro de AuthProvider');
  }
  
  return context;
};

export default AuthContext;
