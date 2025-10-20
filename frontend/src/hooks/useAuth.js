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
    if (!isAuthenticated || !user?.rol) return false;
    return user.rol.nombre === roleName;
  };

  const hasPermission = (permissionName) => {
    if (!isAuthenticated || !user?.rol?.permisos) return false;
    return user.rol.permisos.some(rolPermiso => rolPermiso.permiso.nombre === permissionName);
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
    return user?.rol ? [user.rol] : [];
  };

  const getUserPermissions = () => {
    if (!user?.rol?.permisos) return [];
    return user.rol.permisos.map(rolPermiso => rolPermiso.permiso);
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

    // Funciones básicas - logout directo del contexto
    login: loginWithFeedback,
    logout: logout,
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
    username: user?.nombre_usuario || '',
    fullName: user?.nombre_usuario || '',
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
