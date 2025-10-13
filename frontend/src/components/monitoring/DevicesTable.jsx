/**
 * Componente DevicesTable
 * Tabla avanzada para visualizar y gestionar dispositivos de red
 */
import React, { useState, useEffect, useCallback } from 'react';
import { getDevices, getDeviceInterfaces } from '../../services/monitoringService';

const DevicesTable = () => {
  // Estados principales
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estados de paginación
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage, setItemsPerPage] = useState(20);
  const [totalItems, setTotalItems] = useState(0);
  
  // Estados de filtros
  const [filters, setFilters] = useState({
    search: '',
    tipo_dispositivo: '',
    marca: '',
    zona_geografica: '',
    estado_conexion: '',
    estado_operativo: ''
  });
  
  // Estados de ordenamiento
  const [sortField, setSortField] = useState('device_name');
  const [sortDirection, setSortDirection] = useState('asc');
  
  // Estado de dispositivo seleccionado
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [deviceInterfaces, setDeviceInterfaces] = useState([]);
  const [showDeviceModal, setShowDeviceModal] = useState(false);

  // Función para cargar dispositivos
  const loadDevices = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const apiFilters = {
        ...filters,
        ordering: sortDirection === 'desc' ? `-${sortField}` : sortField
      };
      
      const result = await getDevices(apiFilters, skip, itemsPerPage);
      
      if (result.success) {
        setDevices(result.data);
        setTotalItems(result.total);
      } else {
        setError(result.message);
        setDevices([]);
      }
    } catch (error) {
      setError('Error inesperado al cargar los dispositivos');
      setDevices([]);
    } finally {
      setLoading(false);
    }
  }, [currentPage, itemsPerPage, filters, sortField, sortDirection]);

  // Efecto para cargar datos
  useEffect(() => {
    loadDevices();
  }, [loadDevices]);

  // Función para manejar cambios en filtros
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
    setCurrentPage(1); // Resetear a la primera página
  };

  // Función para manejar ordenamiento
  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(prev => prev === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('asc');
    }
    setCurrentPage(1);
  };

  // Función para mostrar detalles del dispositivo
  const handleDeviceDetails = async (device) => {
    setSelectedDevice(device);
    setShowDeviceModal(true);
    
    // Cargar interfaces del dispositivo
    try {
      const result = await getDeviceInterfaces(device.id);
      if (result.success) {
        setDeviceInterfaces(result.data);
      }
    } catch (error) {
      console.error('Error cargando interfaces:', error);
    }
  };

  // Función para obtener el ícono de estado
  const getStatusIcon = (estado) => {
    const statusMap = {
      'activo': '🟢',
      'inactivo': '🔴',
      'mantenimiento': '🟡',
      'error': '🔴',
      'conectado': '🟢',
      'desconectado': '🔴',
      'warning': '🟡'
    };
    return statusMap[estado?.toLowerCase()] || '⚪';
  };

  // Función para obtener clase CSS de estado
  const getStatusClass = (estado) => {
    const statusMap = {
      'activo': 'status-active',
      'conectado': 'status-active',
      'inactivo': 'status-inactive',
      'desconectado': 'status-inactive',
      'mantenimiento': 'status-warning',
      'warning': 'status-warning',
      'error': 'status-error'
    };
    return statusMap[estado?.toLowerCase()] || 'status-unknown';
  };

  // Calcular paginación
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="devices-table-container">
      {/* Header con título y estadísticas */}
      <div className="table-header">
        <div className="header-title">
          <h2>📱 Dispositivos de Red</h2>
          <p>Gestión y monitoreo de dispositivos en tiempo real</p>
        </div>
        <div className="header-stats">
          <div className="stat-card">
            <span className="stat-number">{totalItems}</span>
            <span className="stat-label">Total Dispositivos</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{devices.filter(d => d.estado_conexion === 'conectado').length}</span>
            <span className="stat-label">Conectados</span>
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="filters-section">
        <div className="filters-grid">
          <input
            type="text"
            placeholder="🔍 Buscar dispositivo..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          <select
            value={filters.tipo_dispositivo}
            onChange={(e) => handleFilterChange('tipo_dispositivo', e.target.value)}
            className="filter-select"
          >
            <option value="">Todos los tipos</option>
            <option value="router">Router</option>
            <option value="switch">Switch</option>
            <option value="firewall">Firewall</option>
            <option value="access_point">Access Point</option>
            <option value="servidor">Servidor</option>
          </select>

          <select
            value={filters.marca}
            onChange={(e) => handleFilterChange('marca', e.target.value)}
            className="filter-select"
          >
            <option value="">Todas las marcas</option>
            <option value="Cisco">Cisco</option>
            <option value="Huawei">Huawei</option>
            <option value="Juniper">Juniper</option>
            <option value="HP">HP</option>
            <option value="Dell">Dell</option>
          </select>

          <select
            value={filters.estado_conexion}
            onChange={(e) => handleFilterChange('estado_conexion', e.target.value)}
            className="filter-select"
          >
            <option value="">Todos los estados</option>
            <option value="conectado">Conectado</option>
            <option value="desconectado">Desconectado</option>
          </select>

          <input
            type="text"
            placeholder="Zona geográfica"
            value={filters.zona_geografica}
            onChange={(e) => handleFilterChange('zona_geografica', e.target.value)}
            className="filter-input"
          />

          <button 
            onClick={() => {
              setFilters({
                search: '',
                tipo_dispositivo: '',
                marca: '',
                zona_geografica: '',
                estado_conexion: '',
                estado_operativo: ''
              });
              setCurrentPage(1);
            }}
            className="btn-clear-filters"
          >
            🗑️ Limpiar
          </button>
        </div>
      </div>

      {/* Control de elementos por página */}
      <div className="table-controls">
        <div className="items-per-page">
          <label>Mostrar:</label>
          <select
            value={itemsPerPage}
            onChange={(e) => {
              setItemsPerPage(Number(e.target.value));
              setCurrentPage(1);
            }}
          >
            <option value={10}>10</option>
            <option value={20}>20</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
          <span>elementos</span>
        </div>
        
        <div className="table-info">
          Mostrando {startItem} - {endItem} de {totalItems} dispositivos
        </div>
      </div>

      {/* Tabla */}
      <div className="table-wrapper">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Cargando dispositivos...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <p>❌ {error}</p>
            <button onClick={loadDevices} className="btn-retry">
              🔄 Reintentar
            </button>
          </div>
        ) : (
          <table className="devices-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('device_name')} className="sortable">
                  Dispositivo {sortField === 'device_name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('tipo_dispositivo')} className="sortable">
                  Tipo {sortField === 'tipo_dispositivo' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('ip_address')} className="sortable">
                  IP Address {sortField === 'ip_address' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('marca')} className="sortable">
                  Marca {sortField === 'marca' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Estado Conexión</th>
                <th>Estado Operativo</th>
                <th onClick={() => handleSort('zona_geografica')} className="sortable">
                  Zona {sortField === 'zona_geografica' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Ubicación</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {devices.map((device) => (
                <tr key={device.id} className="device-row">
                  <td className="device-name">
                    <strong>{device.device_name}</strong>
                    <small>{device.descripcion}</small>
                  </td>
                  <td className="device-type">
                    <span className={`type-badge type-${device.tipo_dispositivo}`}>
                      {device.tipo_dispositivo}
                    </span>
                  </td>
                  <td className="ip-address">{device.ip_address}</td>
                  <td>{device.marca} {device.modelo && <small>({device.modelo})</small>}</td>
                  <td>
                    <span className={`status-badge ${getStatusClass(device.estado_conexion)}`}>
                      {getStatusIcon(device.estado_conexion)} {device.estado_conexion}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge ${getStatusClass(device.estado_operativo)}`}>
                      {getStatusIcon(device.estado_operativo)} {device.estado_operativo}
                    </span>
                  </td>
                  <td>{device.zona_geografica}</td>
                  <td className="location">
                    {device.ubicacion_fisica}
                    {device.latitud && device.longitud && (
                      <small>
                        📍 {device.latitud}, {device.longitud}
                      </small>
                    )}
                  </td>
                  <td className="actions">
                    <button
                      onClick={() => handleDeviceDetails(device)}
                      className="btn-action btn-details"
                      title="Ver detalles"
                    >
                      👁️
                    </button>
                    <button
                      className="btn-action btn-monitor"
                      title="Monitorear"
                    >
                      📊
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Paginación */}
      {!loading && !error && totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
            disabled={currentPage === 1}
            className="btn-page"
          >
            ⬅️ Anterior
          </button>
          
          <div className="page-numbers">
            {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
              const pageNum = Math.max(1, currentPage - 2) + i;
              if (pageNum <= totalPages) {
                return (
                  <button
                    key={pageNum}
                    onClick={() => setCurrentPage(pageNum)}
                    className={`btn-page ${currentPage === pageNum ? 'active' : ''}`}
                  >
                    {pageNum}
                  </button>
                );
              }
              return null;
            })}
          </div>
          
          <button
            onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="btn-page"
          >
            Siguiente ➡️
          </button>
        </div>
      )}

      {/* Modal de detalles del dispositivo */}
      {showDeviceModal && selectedDevice && (
        <div className="modal-overlay" onClick={() => setShowDeviceModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>📱 Detalles del Dispositivo</h3>
              <button 
                onClick={() => setShowDeviceModal(false)}
                className="btn-close"
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="device-info-grid">
                <div className="info-section">
                  <h4>Información General</h4>
                  <div className="info-item">
                    <strong>Nombre:</strong> {selectedDevice.device_name}
                  </div>
                  <div className="info-item">
                    <strong>Tipo:</strong> {selectedDevice.tipo_dispositivo}
                  </div>
                  <div className="info-item">
                    <strong>IP:</strong> {selectedDevice.ip_address}
                  </div>
                  <div className="info-item">
                    <strong>Marca:</strong> {selectedDevice.marca}
                  </div>
                  <div className="info-item">
                    <strong>Modelo:</strong> {selectedDevice.modelo}
                  </div>
                </div>

                <div className="info-section">
                  <h4>Estado y Ubicación</h4>
                  <div className="info-item">
                    <strong>Estado Conexión:</strong>
                    <span className={`status-badge ${getStatusClass(selectedDevice.estado_conexion)}`}>
                      {getStatusIcon(selectedDevice.estado_conexion)} {selectedDevice.estado_conexion}
                    </span>
                  </div>
                  <div className="info-item">
                    <strong>Estado Operativo:</strong>
                    <span className={`status-badge ${getStatusClass(selectedDevice.estado_operativo)}`}>
                      {getStatusIcon(selectedDevice.estado_operativo)} {selectedDevice.estado_operativo}
                    </span>
                  </div>
                  <div className="info-item">
                    <strong>Zona:</strong> {selectedDevice.zona_geografica}
                  </div>
                  <div className="info-item">
                    <strong>Ubicación:</strong> {selectedDevice.ubicacion_fisica}
                  </div>
                </div>
              </div>

              {deviceInterfaces.length > 0 && (
                <div className="interfaces-section">
                  <h4>Interfaces ({deviceInterfaces.length})</h4>
                  <div className="interfaces-grid">
                    {deviceInterfaces.slice(0, 6).map((iface, index) => (
                      <div key={index} className="interface-card">
                        <div className="interface-name">{iface.interface_name}</div>
                        <div className="interface-type">{iface.interface_type}</div>
                        <div className={`interface-status ${getStatusClass(iface.estado_operativo)}`}>
                          {getStatusIcon(iface.estado_operativo)} {iface.estado_operativo}
                        </div>
                      </div>
                    ))}
                  </div>
                  {deviceInterfaces.length > 6 && (
                    <p className="interfaces-more">
                      ... y {deviceInterfaces.length - 6} interfaces más
                    </p>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Estilos CSS */}
      <style>{`
        .devices-table-container {
          padding: 1.5rem;
          background: white;
          border-radius: 12px;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
          margin: 1rem;
        }

        .table-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: 2rem;
          padding-bottom: 1rem;
          border-bottom: 2px solid #f0f0f0;
        }

        .header-title h2 {
          margin: 0 0 0.5rem 0;
          color: #333;
          font-size: 1.8rem;
        }

        .header-title p {
          margin: 0;
          color: #666;
          font-size: 1rem;
        }

        .header-stats {
          display: flex;
          gap: 1rem;
        }

        .stat-card {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem;
          border-radius: 8px;
          text-align: center;
          min-width: 120px;
        }

        .stat-number {
          display: block;
          font-size: 2rem;
          font-weight: bold;
          margin-bottom: 0.25rem;
        }

        .stat-label {
          font-size: 0.9rem;
          opacity: 0.9;
        }

        .filters-section {
          margin-bottom: 1.5rem;
        }

        .filters-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          align-items: center;
        }

        .filter-input, .filter-select {
          padding: 0.75rem;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          font-size: 1rem;
          transition: border-color 0.2s;
        }

        .filter-input:focus, .filter-select:focus {
          border-color: #667eea;
          outline: none;
        }

        .btn-clear-filters {
          padding: 0.75rem 1rem;
          background: #f8f9fa;
          border: 2px solid #e0e0e0;
          border-radius: 8px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-clear-filters:hover {
          background: #e9ecef;
          border-color: #ccc;
        }

        .table-controls {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 1rem;
          padding: 0.75rem;
          background: #f8f9fa;
          border-radius: 8px;
        }

        .items-per-page {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .items-per-page select {
          padding: 0.25rem 0.5rem;
          border: 1px solid #ccc;
          border-radius: 4px;
        }

        .table-info {
          color: #666;
          font-size: 0.9rem;
        }

        .table-wrapper {
          overflow-x: auto;
          border: 1px solid #e0e0e0;
          border-radius: 8px;
        }

        .devices-table {
          width: 100%;
          border-collapse: collapse;
          background: white;
        }

        .devices-table th {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 0.75rem;
          text-align: left;
          font-weight: 600;
          position: sticky;
          top: 0;
          z-index: 10;
        }

        .devices-table th.sortable {
          cursor: pointer;
          user-select: none;
          transition: background-color 0.2s;
        }

        .devices-table th.sortable:hover {
          background: rgba(102, 126, 234, 0.9);
        }

        .devices-table td {
          padding: 0.75rem;
          border-bottom: 1px solid #f0f0f0;
          vertical-align: top;
        }

        .device-row:hover {
          background: #f8f9fa;
        }

        .device-name {
          min-width: 150px;
        }

        .device-name strong {
          display: block;
          margin-bottom: 0.25rem;
        }

        .device-name small {
          color: #666;
          font-size: 0.8rem;
        }

        .type-badge {
          display: inline-block;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
          text-transform: capitalize;
        }

        .type-router { background: #e3f2fd; color: #1976d2; }
        .type-switch { background: #f3e5f5; color: #7b1fa2; }
        .type-firewall { background: #ffebee; color: #d32f2f; }
        .type-access_point { background: #e8f5e8; color: #388e3c; }
        .type-servidor { background: #fff3e0; color: #f57c00; }

        .ip-address {
          font-family: 'Courier New', monospace;
          font-size: 0.9rem;
        }

        .status-badge {
          display: inline-flex;
          align-items: center;
          gap: 0.25rem;
          padding: 0.25rem 0.5rem;
          border-radius: 12px;
          font-size: 0.8rem;
          font-weight: 500;
        }

        .status-active { background: #e8f5e8; color: #2e7d32; }
        .status-inactive { background: #ffebee; color: #c62828; }
        .status-warning { background: #fff8e1; color: #ef6c00; }
        .status-error { background: #ffebee; color: #c62828; }
        .status-unknown { background: #f5f5f5; color: #757575; }

        .location small {
          display: block;
          color: #666;
          font-size: 0.8rem;
          margin-top: 0.25rem;
        }

        .actions {
          white-space: nowrap;
        }

        .btn-action {
          padding: 0.5rem;
          margin: 0 0.25rem;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
          font-size: 1rem;
        }

        .btn-details {
          background: #e3f2fd;
          color: #1976d2;
        }

        .btn-details:hover {
          background: #bbdefb;
        }

        .btn-monitor {
          background: #e8f5e8;
          color: #388e3c;
        }

        .btn-monitor:hover {
          background: #c8e6c9;
        }

        .loading-container, .error-container {
          text-align: center;
          padding: 3rem;
        }

        .spinner {
          border: 4px solid #f3f3f3;
          border-top: 4px solid #667eea;
          border-radius: 50%;
          width: 40px;
          height: 40px;
          animation: spin 1s linear infinite;
          margin: 0 auto 1rem;
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        .btn-retry {
          padding: 0.75rem 1.5rem;
          background: #667eea;
          color: white;
          border: none;
          border-radius: 6px;
          cursor: pointer;
          margin-top: 1rem;
        }

        .pagination {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 0.5rem;
          margin-top: 2rem;
          padding: 1rem;
        }

        .btn-page {
          padding: 0.5rem 1rem;
          border: 2px solid #e0e0e0;
          background: white;
          border-radius: 6px;
          cursor: pointer;
          transition: all 0.2s;
        }

        .btn-page:hover:not(:disabled) {
          border-color: #667eea;
          background: #f8f9ff;
        }

        .btn-page.active {
          background: #667eea;
          color: white;
          border-color: #667eea;
        }

        .btn-page:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .page-numbers {
          display: flex;
          gap: 0.25rem;
        }

        /* Modal Styles */
        .modal-overlay {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0, 0, 0, 0.5);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 1000;
        }

        .modal-content {
          background: white;
          border-radius: 12px;
          max-width: 800px;
          max-height: 90vh;
          overflow-y: auto;
          margin: 1rem;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .modal-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 1.5rem;
          border-bottom: 1px solid #e0e0e0;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border-radius: 12px 12px 0 0;
        }

        .modal-header h3 {
          margin: 0;
        }

        .btn-close {
          background: rgba(255, 255, 255, 0.2);
          border: none;
          color: white;
          font-size: 1.5rem;
          width: 40px;
          height: 40px;
          border-radius: 50%;
          cursor: pointer;
          transition: background 0.2s;
        }

        .btn-close:hover {
          background: rgba(255, 255, 255, 0.3);
        }

        .modal-body {
          padding: 1.5rem;
        }

        .device-info-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 2rem;
          margin-bottom: 2rem;
        }

        .info-section h4 {
          margin: 0 0 1rem 0;
          color: #333;
          border-bottom: 2px solid #f0f0f0;
          padding-bottom: 0.5rem;
        }

        .info-item {
          margin-bottom: 0.75rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .info-item strong {
          min-width: 120px;
          color: #555;
        }

        .interfaces-section h4 {
          margin: 0 0 1rem 0;
          color: #333;
        }

        .interfaces-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .interface-card {
          background: #f8f9fa;
          padding: 1rem;
          border-radius: 8px;
          border-left: 4px solid #667eea;
        }

        .interface-name {
          font-weight: 600;
          margin-bottom: 0.25rem;
        }

        .interface-type {
          font-size: 0.9rem;
          color: #666;
          margin-bottom: 0.5rem;
        }

        .interface-status {
          font-size: 0.8rem;
        }

        .interfaces-more {
          text-align: center;
          color: #666;
          font-style: italic;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .devices-table-container {
            margin: 0.5rem;
            padding: 1rem;
          }

          .table-header {
            flex-direction: column;
            gap: 1rem;
          }

          .header-stats {
            flex-direction: row;
            width: 100%;
          }

          .stat-card {
            flex: 1;
            min-width: auto;
          }

          .filters-grid {
            grid-template-columns: 1fr;
          }

          .table-controls {
            flex-direction: column;
            gap: 1rem;
            text-align: center;
          }

          .devices-table {
            font-size: 0.9rem;
          }

          .devices-table th,
          .devices-table td {
            padding: 0.5rem;
          }

          .device-info-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
          }

          .modal-content {
            margin: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default DevicesTable;
