/**
 * Hook personalizado para autenticación
 * Proporciona una interfaz simplificada para usar el sistema de autenticación
 */
import { useAuthContext } from '../contexts/AuthContext';

/**
 * Hook useAuth
 * @returns {Object} Objeto con estado y funciones de autenticación
 */
export const useAuth = () => {
  const context = useAuthContext();

  if (!context) {
    throw new Error('useAuth debe ser usado dentro de AuthProvider');
  }

  const {
    status,
    user,
    isAuthenticated,
    error,
    isLoading,
    login,
    logout,
    updateUser,
    clearError,
    setError,
    isLoggedIn,
    currentUser,
    authStatus
  } = context;

  // Funciones de utilidad
  const hasRole = (roleName) => {
    if (!isAuthenticated || !user?.roles) return false;
    return user.roles.some(role => role.nombre === roleName);
  };

  const hasPermission = (permissionName) => {
    if (!isAuthenticated || !user?.permisos) return false;
    return user.permisos.some(permiso => permiso.nombre === permissionName);
  };

  const hasAnyRole = (roleNames) => {
    if (!Array.isArray(roleNames)) return false;
    return roleNames.some(roleName => hasRole(roleName));
  };

  const hasAnyPermission = (permissionNames) => {
    if (!Array.isArray(permissionNames)) return false;
    return permissionNames.some(permissionName => hasPermission(permissionName));
  };

  const getUserRoles = () => {
    return user?.roles || [];
  };

  const getUserPermissions = () => {
    return user?.permisos || [];
  };

  const isAdmin = () => {
    return hasRole('Administrador') || hasRole('Super Admin');
  };

  const canAccessRoute = (requiredRoles = [], requiredPermissions = []) => {
    if (!isAuthenticated) return false;
    
    // Si no se requieren roles ni permisos específicos, solo verificar autenticación
    if (requiredRoles.length === 0 && requiredPermissions.length === 0) {
      return true;
    }

    // Verificar si tiene al menos uno de los roles requeridos
    const hasRequiredRole = requiredRoles.length === 0 || hasAnyRole(requiredRoles);
    
    // Verificar si tiene al menos uno de los permisos requeridos
    const hasRequiredPermission = requiredPermissions.length === 0 || hasAnyPermission(requiredPermissions);

    return hasRequiredRole && hasRequiredPermission;
  };

  // Login con manejo de errores mejorado
  const loginWithFeedback = async (credentials) => {
    try {
      const result = await login(credentials);
      
      if (result.success) {
        return {
          success: true,
          message: 'Bienvenido al sistema',
          user: result.user
        };
      } else {
        return {
          success: false,
          message: result.error || 'Error en el login'
        };
      }
    } catch (error) {
      console.error('Error en loginWithFeedback:', error);
      return {
        success: false,
        message: 'Error de conexión'
      };
    }
  };

  // Logout con confirmación
  const logoutWithConfirmation = async (showConfirm = true) => {
    if (showConfirm) {
      const confirmed = window.confirm('¿Estás seguro de que quieres cerrar sesión?');
      if (!confirmed) {
        return { cancelled: true };
      }
    }

    try {
      await logout();
      return { 
        success: true, 
        message: 'Sesión cerrada correctamente' 
      };
    } catch (error) {
      console.error('Error en logout:', error);
      return { 
        success: false, 
        message: 'Error al cerrar sesión' 
      };
    }
  };

  return {
    // Estado básico
    isAuthenticated,
    isLoggedIn,
    user,
    currentUser,
    isLoading,
    error,
    status,
    authStatus,

    // Funciones básicas
    login: loginWithFeedback,
    logout: logoutWithConfirmation,
    updateUser,
    clearError,
    setError,

    // Utilidades de roles y permisos
    hasRole,
    hasPermission,
    hasAnyRole,
    hasAnyPermission,
    getUserRoles,
    getUserPermissions,
    isAdmin,
    canAccessRoute,

    // Información del usuario
    username: user?.username || '',
    fullName: user?.nombre_completo || user?.username || '',
    email: user?.email || '',
    roles: getUserRoles(),
    permissions: getUserPermissions(),

    // Estados derivados
    isAuthenticated: isAuthenticated,
    isUnauthenticated: !isAuthenticated,
    hasUser: !!user,
    hasError: !!error,
    isInitializing: status === 'loading'
  };
};

export default useAuth;
