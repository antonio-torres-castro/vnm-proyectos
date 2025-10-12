/**
 * Componente ProtectedRoute
 * Protege rutas que requieren autenticación y/o permisos específicos
 */
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

/**
 * Componente de carga mientras se verifica la autenticación
 */
const LoadingSpinner = () => (
  <div style={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    flexDirection: 'column'
  }}>
    <div style={{
      border: '4px solid #f3f3f3',
      borderTop: '4px solid #007bff',
      borderRadius: '50%',
      width: '50px',
      height: '50px',
      animation: 'spin 1s linear infinite'
    }}></div>
    <p style={{ marginTop: '1rem', color: '#666' }}>
      Verificando autenticación...
    </p>
    <style jsx>{`
      @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
      }
    `}</style>
  </div>
);

/**
 * Componente de acceso denegado
 */
const AccessDenied = ({ message = "No tienes permisos para acceder a esta página" }) => (
  <div style={{
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    flexDirection: 'column',
    backgroundColor: '#f8f9fa'
  }}>
    <div style={{
      textAlign: 'center',
      padding: '2rem',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      maxWidth: '500px'
    }}>
      <h2 style={{ color: '#dc3545', marginBottom: '1rem' }}>
        🚫 Acceso Denegado
      </h2>
      <p style={{ color: '#666', marginBottom: '1.5rem' }}>
        {message}
      </p>
      <button
        onClick={() => window.history.back()}
        style={{
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          padding: '0.75rem 1.5rem',
          borderRadius: '4px',
          cursor: 'pointer',
          fontSize: '1rem'
        }}
      >
        Volver
      </button>
    </div>
  </div>
);

/**
 * ProtectedRoute Component
 * @param {Object} props - Props del componente
 * @param {React.Component} props.children - Componente hijo a proteger
 * @param {Array<string>} props.requiredRoles - Roles requeridos para acceder
 * @param {Array<string>} props.requiredPermissions - Permisos requeridos para acceder
 * @param {string} props.redirectTo - Ruta de redirección (por defecto: '/login')
 * @param {React.Component} props.fallback - Componente a mostrar si no tiene acceso
 * @param {boolean} props.exact - Si debe coincidir exactamente la ruta
 */
const ProtectedRoute = ({ 
  children, 
  requiredRoles = [], 
  requiredPermissions = [],
  redirectTo = '/login',
  fallback = null,
  exact = false
}) => {
  const { 
    isAuthenticated, 
    isInitializing, 
    canAccessRoute, 
    user 
  } = useAuth();
  
  const location = useLocation();

  // Mostrar loading mientras se inicializa la autenticación
  if (isInitializing) {
    return <LoadingSpinner />;
  }

  // Si no está autenticado, redirigir al login
  if (!isAuthenticated) {
    return (
      <Navigate 
        to={redirectTo} 
        state={{ 
          from: location.pathname,
          message: 'Debes iniciar sesión para acceder a esta página'
        }} 
        replace 
      />
    );
  }

  // Verificar si tiene los roles/permisos requeridos
  const hasAccess = canAccessRoute(requiredRoles, requiredPermissions);

  if (!hasAccess) {
    // Si se proporciona un componente fallback, usarlo
    if (fallback) {
      return fallback;
    }

    // Mensaje personalizado basado en los requisitos
    let accessMessage = "No tienes permisos para acceder a esta página";
    
    if (requiredRoles.length > 0 && requiredPermissions.length > 0) {
      accessMessage = `Se requiere uno de estos roles: ${requiredRoles.join(', ')} y uno de estos permisos: ${requiredPermissions.join(', ')}`;
    } else if (requiredRoles.length > 0) {
      accessMessage = `Se requiere uno de estos roles: ${requiredRoles.join(', ')}`;
    } else if (requiredPermissions.length > 0) {
      accessMessage = `Se requiere uno de estos permisos: ${requiredPermissions.join(', ')}`;
    }

    return <AccessDenied message={accessMessage} />;
  }

  // Si tiene acceso, renderizar el contenido
  return children;
};

/**
 * HOC para proteger componentes
 * @param {React.Component} Component - Componente a proteger
 * @param {Object} options - Opciones de protección
 */
export const withProtectedRoute = (Component, options = {}) => {
  return (props) => (
    <ProtectedRoute {...options}>
      <Component {...props} />
    </ProtectedRoute>
  );
};

/**
 * Componente para rutas que requieren roles específicos
 */
export const RoleProtectedRoute = ({ children, roles, ...props }) => (
  <ProtectedRoute requiredRoles={roles} {...props}>
    {children}
  </ProtectedRoute>
);

/**
 * Componente para rutas que requieren permisos específicos
 */
export const PermissionProtectedRoute = ({ children, permissions, ...props }) => (
  <ProtectedRoute requiredPermissions={permissions} {...props}>
    {children}
  </ProtectedRoute>
);

/**
 * Componente para rutas de administrador
 */
export const AdminRoute = ({ children, ...props }) => (
  <ProtectedRoute requiredRoles={['Administrador', 'Super Admin']} {...props}>
    {children}
  </ProtectedRoute>
);

export default ProtectedRoute;
