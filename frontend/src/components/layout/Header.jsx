/**
 * Componente Header
 * Barra de navegación principal con información del usuario y logout
 */
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';

const Header = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, user, logout, isAdmin, getUserRoles } = useAuth();

  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  // No mostrar header en la página de login
  if (!isAuthenticated || location.pathname === '/login') {
    return null;
  }

  // Protección temporal: Si user es null, mostrar loading
  if (!user) {
    return (
      <header className="header">
        <div className="header-container">
          <div>Cargando usuario...</div>
        </div>
      </header>
    );
  }

  // Manejar logout
  const handleLogout = async () => {
    // Confirmación ANTES de mostrar loading state
    if (!window.confirm('¿Estás seguro de que quieres cerrar sesión?')) {
      return;
    }

    setIsLoggingOut(true);

    try {
      await logout();
      navigate('/login', { replace: true });
    } catch (error) {
      alert('Error inesperado al cerrar sesión');
    } finally {
      setIsLoggingOut(false);
      setShowUserMenu(false);
    }
  };

  // Navegación hacia diferentes secciones
  const handleNavigation = path => {
    navigate(path);
    setShowUserMenu(false);
  };

  // Obtener iniciales del usuario
  const getUserInitials = () => {
    if (!user) return 'U';

    if (user?.nombre_usuario) {
      return user.nombre_usuario
        .split(' ')
        .map(word => word.charAt(0))
        .slice(0, 2)
        .join('')
        .toUpperCase();
    }
    return 'U';
  };

  // Formatear roles para mostrar
  const formatRoles = () => {
    if (!user) return 'Cargando...';

    if (!user.rol) return 'Sin rol asignado';
    return user.rol.nombre;
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo y título */}
        <div
          className="header-brand"
          onClick={() => handleNavigation('/dashboard')}
        >
          <div className="brand-icon">🚀</div>
          <div className="brand-text">
            <h1>VNM Monitor</h1>
            <span>Sistema de Monitoreo</span>
          </div>
        </div>

        {/* Navegación principal */}
        <nav className="header-nav">
          <button
            className={`nav-item ${
              location.pathname === '/dashboard' ? 'active' : ''
            }`}
            onClick={() => handleNavigation('/dashboard')}
          >
            📊 Dashboard
          </button>

          {isAdmin() && (
            <button
              className={`nav-item ${
                location.pathname.startsWith('/admin') ? 'active' : ''
              }`}
              onClick={() => handleNavigation('/admin')}
            >
              ⚙️ Administración
            </button>
          )}

          <button
            className={`nav-item ${
              location.pathname === '/monitoring' ? 'active' : ''
            }`}
            onClick={() => handleNavigation('/monitoring')}
          >
            📡 Monitoreo
          </button>

          <button
            className={`nav-item ${
              location.pathname === '/reports' ? 'active' : ''
            }`}
            onClick={() => handleNavigation('/reports')}
          >
            📈 Reportes
          </button>
        </nav>

        {/* Información del usuario */}
        <div className="header-user">
          <div className="user-info">
            <span className="user-name">
              {user?.nombre_usuario || 'Cargando...'}
            </span>
            <span className="user-role">{formatRoles()}</span>
          </div>

          {/* Avatar con menú desplegable */}
          <div className="user-menu-container">
            <button
              className="user-avatar"
              onClick={() => {
                setShowUserMenu(!showUserMenu);
              }}
              title="Menú de usuario"
            >
              {getUserInitials()}
            </button>

            {/* Menú desplegable */}
            {showUserMenu && (
              <div className="user-dropdown">
                <div className="dropdown-header">
                  <div className="user-avatar-large">{getUserInitials()}</div>
                  <div className="user-details">
                    <strong>{user?.nombre_usuario || 'Usuario'}</strong>
                    <span>{user?.email || 'Sin email'}</span>
                    <small>{formatRoles()}</small>
                  </div>
                </div>

                <div className="dropdown-divider"></div>

                <div className="dropdown-menu">
                  <button
                    className="dropdown-item"
                    onClick={e => {
                      e.stopPropagation();
                      handleNavigation('/profile');
                    }}
                  >
                    👤 Mi Perfil
                  </button>

                  <button
                    className="dropdown-item"
                    onClick={e => {
                      e.stopPropagation();
                      handleNavigation('/settings');
                    }}
                  >
                    ⚙️ Configuración
                  </button>

                  {isAdmin() && (
                    <>
                      <div className="dropdown-divider"></div>
                      <button
                        className="dropdown-item"
                        onClick={e => {
                          e.stopPropagation();
                          handleNavigation('/admin/users');
                        }}
                      >
                        👥 Gestión de Usuarios
                      </button>
                    </>
                  )}

                  <div className="dropdown-divider"></div>

                  <button
                    className={`dropdown-item logout ${
                      isLoggingOut ? 'loading' : ''
                    }`}
                    onClick={e => {
                      e.stopPropagation();
                      handleLogout();
                    }}
                    disabled={isLoggingOut}
                  >
                    {isLoggingOut ? (
                      <>
                        <span className="spinner"></span>
                        Cerrando sesión...
                      </>
                    ) : (
                      <>🚪 Cerrar Sesión</>
                    )}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Overlay para cerrar el menú */}
      {showUserMenu && (
        <div
          className="dropdown-overlay"
          onClick={() => {
            setShowUserMenu(false);
          }}
        ></div>
      )}
    </header>
  );
};

export default Header;
