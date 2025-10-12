/**
 * Dashboard Principal
 * Página principal del sistema una vez autenticado
 */
import React, { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';

const Dashboard = () => {
  const { user, getUserRoles, isAdmin } = useAuth();
  const [currentTime, setCurrentTime] = useState(new Date());

  // Actualizar hora cada segundo
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Estadísticas de ejemplo (en un proyecto real vendrían del backend)
  const mockStats = {
    activeDevices: 247,
    alertsToday: 12,
    networkUptime: 99.8,
    totalUsers: 45
  };

  const formatTime = (date) => {
    return date.toLocaleString('es-ES', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div className="dashboard">
      <div className="dashboard-container">
        {/* Header de bienvenida */}
        <div className="welcome-section">
          <div className="welcome-content">
            <h1>¡Bienvenido de vuelta, {user?.nombre_completo || user?.username}! 👋</h1>
            <p>Sistema de Monitoreo de Red IP - Panel de Control</p>
            <div className="current-time">
              📅 {formatTime(currentTime)}
            </div>
          </div>
          <div className="user-badge">
            <span className="badge-role">
              {getUserRoles()[0]?.nombre || 'Usuario'}
            </span>
          </div>
        </div>

        {/* Tarjetas de estadísticas */}
        <div className="stats-grid">
          <div className="stat-card devices">
            <div className="stat-icon">📡</div>
            <div className="stat-content">
              <h3>Dispositivos Activos</h3>
              <div className="stat-number">{mockStats.activeDevices}</div>
              <div className="stat-subtitle">En la red</div>
            </div>
          </div>

          <div className="stat-card alerts">
            <div className="stat-icon">⚠️</div>
            <div className="stat-content">
              <h3>Alertas Hoy</h3>
              <div className="stat-number">{mockStats.alertsToday}</div>
              <div className="stat-subtitle">Requieren atención</div>
            </div>
          </div>

          <div className="stat-card uptime">
            <div className="stat-icon">✅</div>
            <div className="stat-content">
              <h3>Tiempo de Actividad</h3>
              <div className="stat-number">{mockStats.networkUptime}%</div>
              <div className="stat-subtitle">Últimos 30 días</div>
            </div>
          </div>

          <div className="stat-card users">
            <div className="stat-icon">👥</div>
            <div className="stat-content">
              <h3>Usuarios del Sistema</h3>
              <div className="stat-number">{mockStats.totalUsers}</div>
              <div className="stat-subtitle">Registrados</div>
            </div>
          </div>
        </div>

        {/* Secciones de acciones rápidas */}
        <div className="actions-section">
          <div className="section-title">
            <h2>🚀 Acciones Rápidas</h2>
          </div>
          
          <div className="actions-grid">
            <div className="action-card">
              <div className="action-icon">📊</div>
              <h3>Monitoreo en Tiempo Real</h3>
              <p>Visualiza el estado actual de todos los dispositivos de red</p>
              <button className="action-button">Ver Monitoreo</button>
            </div>

            <div className="action-card">
              <div className="action-icon">📈</div>
              <h3>Reportes de Red</h3>
              <p>Genera reportes detallados de rendimiento y disponibilidad</p>
              <button className="action-button">Generar Reporte</button>
            </div>

            <div className="action-card">
              <div className="action-icon">🔧</div>
              <h3>Configuración</h3>
              <p>Ajusta parámetros de monitoreo y notificaciones</p>
              <button className="action-button">Configurar</button>
            </div>

            {isAdmin() && (
              <div className="action-card admin">
                <div className="action-icon">⚙️</div>
                <h3>Administración</h3>
                <p>Gestiona usuarios, roles y permisos del sistema</p>
                <button className="action-button admin-button">Panel Admin</button>
              </div>
            )}
          </div>
        </div>

        {/* Estado del sistema */}
        <div className="system-status">
          <div className="section-title">
            <h2>📡 Estado del Sistema</h2>
          </div>
          
          <div className="status-grid">
            <div className="status-item healthy">
              <div className="status-indicator"></div>
              <div className="status-content">
                <h4>Servidor Principal</h4>
                <span>Operativo</span>
              </div>
            </div>

            <div className="status-item healthy">
              <div className="status-indicator"></div>
              <div className="status-content">
                <h4>Base de Datos</h4>
                <span>Conectada</span>
              </div>
            </div>

            <div className="status-item warning">
              <div className="status-indicator"></div>
              <div className="status-content">
                <h4>Monitor de Red</h4>
                <span>Carga Alta</span>
              </div>
            </div>

            <div className="status-item healthy">
              <div className="status-indicator"></div>
              <div className="status-content">
                <h4>API Gateway</h4>
                <span>Funcionando</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Estilos CSS embebidos */}
      <style jsx>{`
        .dashboard {
          min-height: calc(100vh - 70px);
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        .dashboard-container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 2rem 1rem;
        }

        .welcome-section {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          margin-bottom: 2rem;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          display: flex;
          justify-content: space-between;
          align-items: center;
          animation: slideUp 0.6s ease-out;
        }

        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .welcome-content h1 {
          color: #333;
          margin: 0 0 0.5rem 0;
          font-size: 2rem;
          font-weight: 700;
        }

        .welcome-content p {
          color: #666;
          margin: 0 0 1rem 0;
          font-size: 1.1rem;
        }

        .current-time {
          color: #888;
          font-size: 0.9rem;
          background: #f8f9fa;
          padding: 0.5rem 1rem;
          border-radius: 6px;
          display: inline-block;
        }

        .user-badge {
          text-align: center;
        }

        .badge-role {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.9rem;
          font-weight: 600;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 1.5rem;
          margin-bottom: 2rem;
        }

        .stat-card {
          background: white;
          border-radius: 12px;
          padding: 1.5rem;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          display: flex;
          align-items: center;
          gap: 1rem;
          transition: transform 0.2s ease;
          animation: slideUp 0.8s ease-out;
        }

        .stat-card:hover {
          transform: translateY(-2px);
        }

        .stat-icon {
          font-size: 2.5rem;
          opacity: 0.8;
        }

        .stat-content h3 {
          margin: 0 0 0.5rem 0;
          color: #333;
          font-size: 1rem;
          font-weight: 600;
        }

        .stat-number {
          font-size: 2rem;
          font-weight: 700;
          color: #667eea;
          margin-bottom: 0.25rem;
        }

        .stat-subtitle {
          color: #888;
          font-size: 0.85rem;
        }

        .section-title {
          margin-bottom: 1.5rem;
        }

        .section-title h2 {
          color: #333;
          font-size: 1.5rem;
          font-weight: 600;
        }

        .actions-section {
          margin-bottom: 2rem;
        }

        .actions-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1.5rem;
        }

        .action-card {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          text-align: center;
          transition: transform 0.2s ease;
          animation: slideUp 1s ease-out;
        }

        .action-card:hover {
          transform: translateY(-4px);
        }

        .action-card.admin {
          background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
          color: #2d3436;
        }

        .action-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
          opacity: 0.8;
        }

        .action-card h3 {
          margin: 0 0 1rem 0;
          color: #333;
          font-size: 1.2rem;
          font-weight: 600;
        }

        .action-card.admin h3 {
          color: #2d3436;
        }

        .action-card p {
          color: #666;
          margin: 0 0 1.5rem 0;
          line-height: 1.5;
        }

        .action-card.admin p {
          color: #636e72;
        }

        .action-button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 0.75rem 1.5rem;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 600;
          transition: all 0.2s ease;
        }

        .action-button:hover {
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }

        .admin-button {
          background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        }

        .admin-button:hover {
          box-shadow: 0 4px 12px rgba(225, 112, 85, 0.3);
        }

        .system-status {
          background: white;
          border-radius: 12px;
          padding: 2rem;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          animation: slideUp 1.2s ease-out;
        }

        .status-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }

        .status-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          padding: 1rem;
          border-radius: 8px;
          background: #f8f9fa;
        }

        .status-indicator {
          width: 12px;
          height: 12px;
          border-radius: 50%;
          flex-shrink: 0;
        }

        .status-item.healthy .status-indicator {
          background: #00b894;
          box-shadow: 0 0 10px rgba(0, 184, 148, 0.3);
        }

        .status-item.warning .status-indicator {
          background: #fdcb6e;
          box-shadow: 0 0 10px rgba(253, 203, 110, 0.3);
        }

        .status-item.error .status-indicator {
          background: #e84393;
          box-shadow: 0 0 10px rgba(232, 67, 147, 0.3);
        }

        .status-content h4 {
          margin: 0 0 0.25rem 0;
          color: #333;
          font-size: 0.9rem;
          font-weight: 600;
        }

        .status-content span {
          color: #666;
          font-size: 0.8rem;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .dashboard-container {
            padding: 1rem 0.5rem;
          }

          .welcome-section {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }

          .welcome-content h1 {
            font-size: 1.5rem;
          }

          .stats-grid {
            grid-template-columns: 1fr;
          }

          .actions-grid {
            grid-template-columns: 1fr;
          }

          .status-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </div>
  );
};

export default Dashboard;
