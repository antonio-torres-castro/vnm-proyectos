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
  const { 
    isAuthenticated, 
    user, 
    logout, 
    isAdmin, 
    getUserRoles 
  } = useAuth();

  const [showUserMenu, setShowUserMenu] = useState(false);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  // No mostrar header en la página de login
  if (!isAuthenticated || location.pathname === '/login') {
    return null;
  }

  // Manejar logout
  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      const result = await logout(true); // Con confirmación
      if (!result.cancelled) {
        navigate('/login', { replace: true });
      }
    } catch (error) {
      console.error('Error en logout:', error);
    } finally {
      setIsLoggingOut(false);
      setShowUserMenu(false);
    }
  };

  // Navegación hacia diferentes secciones
  const handleNavigation = (path) => {
    navigate(path);
    setShowUserMenu(false);
  };

  // Obtener iniciales del usuario
  const getUserInitials = () => {
    if (user?.nombre_completo) {
      return user.nombre_completo
        .split(' ')
        .map(word => word.charAt(0))
        .slice(0, 2)
        .join('')
        .toUpperCase();
    }
    return user?.username?.charAt(0).toUpperCase() || 'U';
  };

  // Formatear roles para mostrar
  const formatRoles = () => {
    const roles = getUserRoles();
    if (roles.length === 0) return 'Sin roles asignados';
    if (roles.length === 1) return roles[0].nombre;
    return `${roles[0].nombre} (+${roles.length - 1})`;
  };

  return (
    <header className="header">
      <div className="header-container">
        {/* Logo y título */}
        <div className="header-brand" onClick={() => handleNavigation('/dashboard')}>
          <div className="brand-icon">🚀</div>
          <div className="brand-text">
            <h1>VNM Monitor</h1>
            <span>Sistema de Monitoreo</span>
          </div>
        </div>

        {/* Navegación principal */}
        <nav className="header-nav">
          <button
            className={`nav-item ${location.pathname === '/dashboard' ? 'active' : ''}`}
            onClick={() => handleNavigation('/dashboard')}
          >
            📊 Dashboard
          </button>
          
          {isAdmin() && (
            <button
              className={`nav-item ${location.pathname.startsWith('/admin') ? 'active' : ''}`}
              onClick={() => handleNavigation('/admin')}
            >
              ⚙️ Administración
            </button>
          )}
          
          <button
            className={`nav-item ${location.pathname === '/monitoring' ? 'active' : ''}`}
            onClick={() => handleNavigation('/monitoring')}
          >
            📡 Monitoreo
          </button>
          
          <button
            className={`nav-item ${location.pathname === '/reports' ? 'active' : ''}`}
            onClick={() => handleNavigation('/reports')}
          >
            📈 Reportes
          </button>
        </nav>

        {/* Información del usuario */}
        <div className="header-user">
          <div className="user-info">
            <span className="user-name">
              {user?.nombre_completo || user?.username || 'Usuario'}
            </span>
            <span className="user-role">
              {formatRoles()}
            </span>
          </div>

          {/* Avatar con menú desplegable */}
          <div className="user-menu-container">
            <button
              className="user-avatar"
              onClick={() => setShowUserMenu(!showUserMenu)}
              title="Menú de usuario"
            >
              {getUserInitials()}
            </button>

            {/* Menú desplegable */}
            {showUserMenu && (
              <div className="user-dropdown">
                <div className="dropdown-header">
                  <div className="user-avatar-large">
                    {getUserInitials()}
                  </div>
                  <div className="user-details">
                    <strong>{user?.nombre_completo || user?.username}</strong>
                    <span>{user?.email || 'Sin email'}</span>
                    <small>{formatRoles()}</small>
                  </div>
                </div>

                <div className="dropdown-divider"></div>

                <div className="dropdown-menu">
                  <button
                    className="dropdown-item"
                    onClick={() => handleNavigation('/profile')}
                  >
                    👤 Mi Perfil
                  </button>
                  
                  <button
                    className="dropdown-item"
                    onClick={() => handleNavigation('/settings')}
                  >
                    ⚙️ Configuración
                  </button>

                  {isAdmin() && (
                    <>
                      <div className="dropdown-divider"></div>
                      <button
                        className="dropdown-item"
                        onClick={() => handleNavigation('/admin/users')}
                      >
                        👥 Gestión de Usuarios
                      </button>
                    </>
                  )}

                  <div className="dropdown-divider"></div>
                  
                  <button
                    className={`dropdown-item logout ${isLoggingOut ? 'loading' : ''}`}
                    onClick={handleLogout}
                    disabled={isLoggingOut}
                  >
                    {isLoggingOut ? (
                      <>
                        <span className="spinner"></span>
                        Cerrando sesión...
                      </>
                    ) : (
                      <>
                        🚪 Cerrar Sesión
                      </>
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
          onClick={() => setShowUserMenu(false)}
        ></div>
      )}

      {/* Estilos CSS embebidos */}
      <style>{`
        .header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          position: sticky;
          top: 0;
          z-index: 1000;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .header-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
          height: 70px;
        }

        .header-brand {
          display: flex;
          align-items: center;
          gap: 1rem;
          cursor: pointer;
          transition: opacity 0.2s ease;
        }

        .header-brand:hover {
          opacity: 0.9;
        }

        .brand-icon {
          font-size: 2rem;
          filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
        }

        .brand-text h1 {
          margin: 0;
          font-size: 1.5rem;
          font-weight: 700;
        }

        .brand-text span {
          font-size: 0.8rem;
          opacity: 0.9;
          display: block;
          margin-top: -2px;
        }

        .header-nav {
          display: flex;
          gap: 0.5rem;
          flex-grow: 1;
          justify-content: center;
        }

        .nav-item {
          background: rgba(255, 255, 255, 0.1);
          border: none;
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s ease;
          font-size: 0.9rem;
          font-weight: 500;
          backdrop-filter: blur(10px);
        }

        .nav-item:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-1px);
        }

        .nav-item.active {
          background: rgba(255, 255, 255, 0.25);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }

        .header-user {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .user-info {
          text-align: right;
          display: flex;
          flex-direction: column;
        }

        .user-name {
          font-weight: 600;
          font-size: 0.9rem;
        }

        .user-role {
          font-size: 0.75rem;
          opacity: 0.8;
        }

        .user-menu-container {
          position: relative;
        }

        .user-avatar {
          width: 45px;
          height: 45px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.2);
          border: 2px solid rgba(255, 255, 255, 0.3);
          color: white;
          font-weight: 700;
          font-size: 1rem;
          cursor: pointer;
          transition: all 0.2s ease;
          backdrop-filter: blur(10px);
        }

        .user-avatar:hover {
          background: rgba(255, 255, 255, 0.3);
          transform: scale(1.05);
        }

        .user-dropdown {
          position: absolute;
          top: calc(100% + 10px);
          right: 0;
          background: white;
          border-radius: 12px;
          box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
          min-width: 280px;
          overflow: hidden;
          animation: slideDown 0.2s ease-out;
        }

        @keyframes slideDown {
          from {
            opacity: 0;
            transform: translateY(-10px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .dropdown-header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1.5rem;
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .user-avatar-large {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background: rgba(255, 255, 255, 0.2);
          border: 2px solid rgba(255, 255, 255, 0.3);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: 700;
          font-size: 1.1rem;
        }

        .user-details {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .user-details strong {
          font-size: 1rem;
        }

        .user-details span {
          font-size: 0.85rem;
          opacity: 0.9;
        }

        .user-details small {
          font-size: 0.75rem;
          opacity: 0.8;
        }

        .dropdown-divider {
          height: 1px;
          background: #eee;
          margin: 0.5rem 0;
        }

        .dropdown-menu {
          padding: 0.5rem 0;
        }

        .dropdown-item {
          width: 100%;
          background: none;
          border: none;
          text-align: left;
          padding: 0.75rem 1.5rem;
          cursor: pointer;
          transition: background-color 0.2s ease;
          font-size: 0.9rem;
          color: #333;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .dropdown-item:hover {
          background: #f8f9fa;
        }

        .dropdown-item.logout {
          color: #dc3545;
        }

        .dropdown-item.logout:hover {
          background: #fff5f5;
        }

        .dropdown-item:disabled {
          cursor: not-allowed;
          opacity: 0.6;
        }

        .dropdown-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: transparent;
          z-index: 999;
        }

        .spinner {
          width: 12px;
          height: 12px;
          border: 2px solid transparent;
          border-top: 2px solid currentColor;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        @keyframes spin {
          to {
            transform: rotate(360deg);
          }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .header-container {
            padding: 0 0.5rem;
          }

          .brand-text span {
            display: none;
          }

          .header-nav {
            gap: 0.25rem;
          }

          .nav-item {
            padding: 0.5rem 0.75rem;
            font-size: 0.8rem;
          }

          .user-info {
            display: none;
          }

          .user-dropdown {
            min-width: 250px;
          }
        }
      `}</style>
    </header>
  );
};

export default Header;
