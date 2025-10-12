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
            className="action-button primary"
            onClick={handleGoHome}
          >
            <span className="button-icon">🏠</span>
            {isAuthenticated ? 'Ir al Dashboard' : 'Ir al Inicio'}
          </button>

          <button 
            className="action-button secondary"
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

      {/* Estilos CSS embebidos */}
      <style jsx>{`
        .not-found {
          min-height: 100vh;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
        }

        .not-found-container {
          background: white;
          border-radius: 20px;
          padding: 3rem;
          max-width: 600px;
          width: 100%;
          text-align: center;
          box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
          animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .error-animation {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 1rem;
          margin-bottom: 2rem;
          animation: bounce 2s ease-in-out infinite;
        }

        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-10px);
          }
          60% {
            transform: translateY(-5px);
          }
        }

        .error-number {
          font-size: 6rem;
          font-weight: 900;
          color: #667eea;
          text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .error-icon {
          font-size: 4rem;
          animation: spin 3s linear infinite;
        }

        @keyframes spin {
          from {
            transform: rotate(0deg);
          }
          to {
            transform: rotate(360deg);
          }
        }

        .error-content h1 {
          color: #333;
          font-size: 2rem;
          margin: 0 0 1rem 0;
          font-weight: 700;
        }

        .error-content p {
          color: #666;
          font-size: 1.1rem;
          line-height: 1.6;
          margin: 0 0 2rem 0;
        }

        .error-details {
          background: #f8f9fa;
          border-radius: 12px;
          padding: 1.5rem;
          margin-bottom: 2rem;
          text-align: left;
        }

        .detail-item {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1rem;
          font-size: 0.95rem;
          color: #555;
        }

        .detail-item:last-child {
          margin-bottom: 0;
        }

        .detail-icon {
          font-size: 1.2rem;
          width: 1.5rem;
          text-align: center;
        }

        .error-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
          margin-bottom: 2rem;
        }

        .action-button {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 1rem 2rem;
          border-radius: 10px;
          border: none;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.2s ease;
          min-width: 160px;
          justify-content: center;
        }

        .action-button.primary {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
        }

        .action-button.primary:hover {
          transform: translateY(-2px);
          box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        }

        .action-button.secondary {
          background: #f8f9fa;
          color: #333;
          border: 2px solid #e9ecef;
        }

        .action-button.secondary:hover {
          background: #e9ecef;
          transform: translateY(-1px);
        }

        .button-icon {
          font-size: 1.1rem;
        }

        .navigation-help {
          border-top: 1px solid #eee;
          padding-top: 2rem;
          margin-top: 2rem;
        }

        .navigation-help h3 {
          color: #333;
          font-size: 1.2rem;
          margin: 0 0 1rem 0;
          font-weight: 600;
        }

        .nav-suggestions {
          display: flex;
          gap: 0.75rem;
          flex-wrap: wrap;
          justify-content: center;
        }

        .nav-suggestion {
          background: #f8f9fa;
          border: 1px solid #e9ecef;
          border-radius: 6px;
          padding: 0.5rem 1rem;
          font-size: 0.9rem;
          cursor: pointer;
          transition: all 0.2s ease;
          color: #555;
        }

        .nav-suggestion:hover {
          background: #667eea;
          color: white;
          transform: translateY(-1px);
        }

        /* Responsive */
        @media (max-width: 768px) {
          .not-found-container {
            padding: 2rem 1.5rem;
            margin: 1rem;
          }

          .error-number {
            font-size: 4rem;
          }

          .error-icon {
            font-size: 3rem;
          }

          .error-content h1 {
            font-size: 1.6rem;
          }

          .error-content p {
            font-size: 1rem;
          }

          .error-actions {
            flex-direction: column;
            align-items: center;
          }

          .action-button {
            width: 100%;
            max-width: 280px;
          }

          .nav-suggestions {
            flex-direction: column;
            align-items: center;
          }

          .nav-suggestion {
            width: 100%;
            max-width: 200px;
            text-align: center;
          }
        }

        @media (max-width: 480px) {
          .error-animation {
            gap: 0.5rem;
          }

          .error-number {
            font-size: 3rem;
          }

          .error-icon {
            font-size: 2rem;
          }
        }
      `}</style>
    </div>
  );
};

export default NotFound;
