/**
 * Página de Monitoreo
 * Dashboard principal para el módulo de monitoreo de red
 */
import React, { useState, useEffect } from 'react';
import DevicesTable from '../components/monitoring/DevicesTable';
import InterfacesTable from '../components/monitoring/InterfacesTable';
import { getMonitoringStats } from '../services/monitoringService';

const MonitoringPage = () => {
  const [stats, setStats] = useState({
    totalDevices: 0,
    totalInterfaces: 0,
    avgInterfacesPerDevice: 0
  });
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('devices');

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const result = await getMonitoringStats();
      if (result.success) {
        setStats(result.data);
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="monitoring-page">
      {/* Hero Section */}
      <div className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>📡 Centro de Monitoreo de Red</h1>
            <p>Supervisión y gestión integral de dispositivos e interfaces de red en tiempo real</p>
          </div>
          <div className="hero-stats">
            {loading ? (
              <div className="stats-loading">
                <div className="spinner-small"></div>
                <span>Cargando estadísticas...</span>
              </div>
            ) : (
              <>
                <div className="stat-item">
                  <div className="stat-icon">📱</div>
                  <div className="stat-content">
                    <span className="stat-number">{stats.totalDevices}</span>
                    <span className="stat-label">Dispositivos</span>
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-icon">🔌</div>
                  <div className="stat-content">
                    <span className="stat-number">{stats.totalInterfaces}</span>
                    <span className="stat-label">Interfaces</span>
                  </div>
                </div>
                <div className="stat-item">
                  <div className="stat-icon">📊</div>
                  <div className="stat-content">
                    <span className="stat-number">{stats.avgInterfacesPerDevice}</span>
                    <span className="stat-label">Promedio Int./Dev.</span>
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tabs-container">
        <div className="tabs-wrapper">
          <button
            className={`tab-button ${activeTab === 'devices' ? 'active' : ''}`}
            onClick={() => setActiveTab('devices')}
          >
            📱 Dispositivos
          </button>
          <button
            className={`tab-button ${activeTab === 'interfaces' ? 'active' : ''}`}
            onClick={() => setActiveTab('interfaces')}
          >
            🔌 Interfaces
          </button>
          <button
            className={`tab-button ${activeTab === 'topology' ? 'active' : ''}`}
            onClick={() => setActiveTab('topology')}
          >
            🗺️ Topología
          </button>
          <button
            className={`tab-button ${activeTab === 'alerts' ? 'active' : ''}`}
            onClick={() => setActiveTab('alerts')}
          >
            🚨 Alertas
          </button>
        </div>
      </div>

      {/* Content Area */}
      <div className="content-area">
        {activeTab === 'devices' && (
          <div className="tab-content">
            <DevicesTable />
          </div>
        )}

        {activeTab === 'interfaces' && (
          <div className="tab-content">
            <InterfacesTable />
          </div>
        )}

        {activeTab === 'topology' && (
          <div className="tab-content">
            <div className="placeholder-content">
              <div className="placeholder-icon">🗺️</div>
              <h3>Mapa de Topología de Red</h3>
              <p>El mapa interactivo de topología estará disponible próximamente.</p>
              <p>Visualiza la estructura completa de tu red con conexiones en tiempo real.</p>
              <div className="features-preview">
                <h4>Características planeadas:</h4>
                <ul>
                  <li>🌐 Mapa interactivo de la red</li>
                  <li>🔗 Visualización de conexiones físicas</li>
                  <li>📍 Ubicación geográfica de dispositivos</li>
                  <li>🎨 Estados visuales en tiempo real</li>
                  <li>🔍 Zoom y navegación intuitiva</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'alerts' && (
          <div className="tab-content">
            <div className="placeholder-content">
              <div className="placeholder-icon">🚨</div>
              <h3>Centro de Alertas</h3>
              <p>El sistema de alertas inteligente estará disponible próximamente.</p>
              <p>Recibe notificaciones automáticas sobre el estado de tu infraestructura.</p>
              <div className="features-preview">
                <h4>Características planeadas:</h4>
                <ul>
                  <li>⚡ Alertas en tiempo real</li>
                  <li>📧 Notificaciones por email</li>
                  <li>📱 Integración con móviles</li>
                  <li>🎯 Reglas personalizables</li>
                  <li>📊 Dashboard de incidencias</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Estilos CSS */}
      <style>{`
        .monitoring-page {
          min-height: 100vh;
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }

        .hero-section {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 3rem 1rem;
          margin-bottom: 2rem;
        }

        .hero-content {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          justify-content: space-between;
          align-items: center;
          gap: 2rem;
        }

        .hero-text h1 {
          margin: 0 0 1rem 0;
          font-size: 2.5rem;
          font-weight: 700;
        }

        .hero-text p {
          margin: 0;
          font-size: 1.2rem;
          opacity: 0.9;
          max-width: 600px;
          line-height: 1.6;
        }

        .hero-stats {
          display: flex;
          gap: 2rem;
          flex-wrap: wrap;
        }

        .stats-loading {
          display: flex;
          align-items: center;
          gap: 1rem;
          color: white;
          opacity: 0.8;
        }

        .spinner-small {
          width: 20px;
          height: 20px;
          border: 2px solid rgba(255, 255, 255, 0.3);
          border-top: 2px solid white;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }

        .stat-item {
          display: flex;
          align-items: center;
          gap: 1rem;
          background: rgba(255, 255, 255, 0.1);
          padding: 1.5rem;
          border-radius: 12px;
          backdrop-filter: blur(10px);
          min-width: 180px;
        }

        .stat-icon {
          font-size: 2.5rem;
          filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
        }

        .stat-content {
          display: flex;
          flex-direction: column;
        }

        .stat-number {
          font-size: 2rem;
          font-weight: bold;
          line-height: 1;
          margin-bottom: 0.25rem;
        }

        .stat-label {
          font-size: 0.9rem;
          opacity: 0.9;
          white-space: nowrap;
        }

        .tabs-container {
          background: white;
          border-bottom: 1px solid #e0e0e0;
          position: sticky;
          top: 70px;
          z-index: 100;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .tabs-wrapper {
          max-width: 1200px;
          margin: 0 auto;
          display: flex;
          padding: 0 1rem;
        }

        .tab-button {
          background: none;
          border: none;
          padding: 1rem 2rem;
          cursor: pointer;
          font-size: 1rem;
          font-weight: 500;
          color: #666;
          border-bottom: 3px solid transparent;
          transition: all 0.2s ease;
          white-space: nowrap;
        }

        .tab-button:hover {
          color: #667eea;
          background: #f8f9ff;
        }

        .tab-button.active {
          color: #667eea;
          border-bottom-color: #667eea;
          background: #f8f9ff;
        }

        .content-area {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 1rem;
        }

        .tab-content {
          margin-top: 2rem;
        }

        .placeholder-content {
          background: white;
          border-radius: 12px;
          padding: 3rem;
          text-align: center;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          margin: 1rem;
        }

        .placeholder-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
          filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
        }

        .placeholder-content h3 {
          margin: 0 0 1rem 0;
          color: #333;
          font-size: 1.8rem;
        }

        .placeholder-content p {
          color: #666;
          font-size: 1.1rem;
          line-height: 1.6;
          margin-bottom: 1rem;
          max-width: 600px;
          margin-left: auto;
          margin-right: auto;
        }

        .features-preview {
          background: #f8f9fa;
          border-radius: 8px;
          padding: 2rem;
          margin-top: 2rem;
          max-width: 500px;
          margin-left: auto;
          margin-right: auto;
        }

        .features-preview h4 {
          margin: 0 0 1rem 0;
          color: #333;
          font-size: 1.2rem;
        }

        .features-preview ul {
          text-align: left;
          color: #555;
          line-height: 1.8;
        }

        .features-preview li {
          margin-bottom: 0.5rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
          .hero-content {
            flex-direction: column;
            text-align: center;
          }

          .hero-text h1 {
            font-size: 2rem;
          }

          .hero-text p {
            font-size: 1rem;
          }

          .hero-stats {
            flex-direction: column;
            gap: 1rem;
            width: 100%;
          }

          .stat-item {
            min-width: auto;
            justify-content: center;
          }

          .tabs-wrapper {
            overflow-x: auto;
            padding: 0 0.5rem;
          }

          .tab-button {
            padding: 1rem 1.5rem;
          }

          .content-area {
            padding: 0 0.5rem;
          }

          .placeholder-content {
            padding: 2rem 1rem;
            margin: 0.5rem;
          }

          .placeholder-icon {
            font-size: 3rem;
          }

          .placeholder-content h3 {
            font-size: 1.5rem;
          }

          .placeholder-content p {
            font-size: 1rem;
          }

          .features-preview {
            padding: 1.5rem;
          }
        }

        @media (max-width: 480px) {
          .hero-section {
            padding: 2rem 1rem;
          }

          .hero-text h1 {
            font-size: 1.8rem;
          }

          .stat-item {
            padding: 1rem;
          }

          .stat-number {
            font-size: 1.5rem;
          }

          .stat-label {
            font-size: 0.8rem;
          }
        }
      `}</style>
    </div>
  );
};

export default MonitoringPage;
