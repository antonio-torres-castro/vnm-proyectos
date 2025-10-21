/**
 * Página 404 - No encontrado
 * Página que se muestra cuando una ruta no existe
 */
import React from 'react';
import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';

const NotFound = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const handleGoHome = () => {
    navigate(isAuthenticated ? '/dashboard' : '/');
  };

  const handleGoBack = () => {
    window.history.back();
  };

  return (
    <div className="not-found">
      <div className="not-found-container">
        <div className="error-animation">
          <div className="error-number">4</div>
          <div className="error-icon">🌐</div>
          <div className="error-number">4</div>
        </div>

        <div className="error-content">
          <h1>¡Oops! Página no encontrada</h1>
          <p>
            La página que estás buscando no existe o ha sido movida. 
            Es posible que hayas ingresado una URL incorrecta o que el enlace esté desactualizado.
          </p>

          <div className="error-details">
            <div className="detail-item">
              <span className="detail-icon">🔍</span>
              <span>Verifica la URL en la barra de direcciones</span>
            </div>
            <div className="detail-item">
              <span className="detail-icon">🔗</span>
              <span>Comprueba que el enlace esté funcionando</span>
            </div>
            <div className="detail-item">
              <span className="detail-icon">⏰</span>
              <span>La página podría haber sido movida recientemente</span>
            </div>
          </div>
        </div>

        <div className="error-actions">
          <button 
            className="btn btn-primary"
            onClick={handleGoHome}
          >
            <span className="button-icon">🏠</span>
            {isAuthenticated ? 'Ir al Dashboard' : 'Ir al Inicio'}
          </button>

          <button 
            className="btn btn-secondary"
            onClick={handleGoBack}
          >
            <span className="button-icon">⬅️</span>
            Página Anterior
          </button>
        </div>

        {/* Información adicional para usuarios autenticados */}
        {isAuthenticated && (
          <div className="navigation-help">
            <h3>💡 Páginas disponibles:</h3>
            <div className="nav-suggestions">
              <button 
                className="nav-suggestion"
                onClick={() => navigate('/dashboard')}
              >
                📊 Dashboard
              </button>
              <button 
                className="nav-suggestion"
                onClick={() => navigate('/monitoring')}
              >
                📡 Monitoreo
              </button>
              <button 
                className="nav-suggestion"
                onClick={() => navigate('/reports')}
              >
                📈 Reportes
              </button>
              <button 
                className="nav-suggestion"
                onClick={() => navigate('/profile')}
              >
                👤 Mi Perfil
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default NotFound;
