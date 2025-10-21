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
    </div>
  );
};

export default MonitoringPage;
