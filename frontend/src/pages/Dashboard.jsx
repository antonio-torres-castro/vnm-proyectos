/**
 * Dashboard Principal
 * Página principal del sistema una vez autenticado
 */
import React, { useEffect, useState } from 'react';
import useAuth from '../hooks/useAuth';
import './Dashboard.css';

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


    </div>
  );
};

export default Dashboard;
