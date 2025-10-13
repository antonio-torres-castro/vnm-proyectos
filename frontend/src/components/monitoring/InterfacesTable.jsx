/**
 * Componente InterfacesTable
 * Tabla avanzada para visualizar y gestionar interfaces de red
 */
import React, { useState, useEffect, useCallback } from 'react';
import { getInterfaces, getDevices } from '../../services/monitoringService';

const InterfacesTable = () => {
  // Estados principales
  const [interfaces, setInterfaces] = useState([]);
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
    interface_type: '',
    estado_administrativo: '',
    estado_operativo: '',
    dispositivo_id: '',
    velocidad: ''
  });
  
  // Estados de ordenamiento
  const [sortField, setSortField] = useState('interface_name');
  const [sortDirection, setSortDirection] = useState('asc');
  
  // Estado de interfaz seleccionada
  const [selectedInterface, setSelectedInterface] = useState(null);
  const [showInterfaceModal, setShowInterfaceModal] = useState(false);

  // Función para cargar dispositivos (para el filtro)
  const loadDevices = useCallback(async () => {
    try {
      const result = await getDevices({}, 0, 1000); // Cargar todos para el filtro
      if (result.success) {
        setDevices(result.data);
      }
    } catch (error) {
      console.error('Error cargando dispositivos:', error);
    }
  }, []);

  // Función para cargar interfaces
  const loadInterfaces = useCallback(async () => {
    setLoading(true);
    setError(null);
    
    try {
      const skip = (currentPage - 1) * itemsPerPage;
      const apiFilters = {
        ...filters,
        ordering: sortDirection === 'desc' ? `-${sortField}` : sortField
      };
      
      const result = await getInterfaces(apiFilters, skip, itemsPerPage);
      
      if (result.success) {
        setInterfaces(result.data);
        setTotalItems(result.total);
      } else {
        setError(result.message);
        setInterfaces([]);
      }
    } catch (error) {
      setError('Error inesperado al cargar las interfaces');
      setInterfaces([]);
    } finally {
      setLoading(false);
    }
  }, [currentPage, itemsPerPage, filters, sortField, sortDirection]);

  // Efectos para cargar datos
  useEffect(() => {
    loadDevices();
  }, [loadDevices]);

  useEffect(() => {
    loadInterfaces();
  }, [loadInterfaces]);

  // Función para manejar cambios en filtros
  const handleFilterChange = (field, value) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
    setCurrentPage(1);
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

  // Función para mostrar detalles de la interfaz
  const handleInterfaceDetails = (interfaceItem) => {
    setSelectedInterface(interfaceItem);
    setShowInterfaceModal(true);
  };

  // Función para obtener el ícono de estado
  const getStatusIcon = (estado) => {
    const statusMap = {
      'up': '🟢',
      'down': '🔴',
      'administratively_down': '🟡',
      'testing': '🟡',
      'enabled': '🟢',
      'disabled': '🔴',
      'activo': '🟢',
      'inactivo': '🔴'
    };
    return statusMap[estado?.toLowerCase()] || '⚪';
  };

  // Función para obtener clase CSS de estado
  const getStatusClass = (estado) => {
    const statusMap = {
      'up': 'status-active',
      'enabled': 'status-active',
      'activo': 'status-active',
      'down': 'status-inactive',
      'disabled': 'status-inactive',
      'inactivo': 'status-inactive',
      'administratively_down': 'status-warning',
      'testing': 'status-warning'
    };
    return statusMap[estado?.toLowerCase()] || 'status-unknown';
  };

  // Función para formatear velocidad
  const formatSpeed = (speed) => {
    if (!speed) return 'N/A';
    const speedNum = parseInt(speed);
    if (speedNum >= 1000000000) return `${(speedNum / 1000000000).toFixed(1)}G`;
    if (speedNum >= 1000000) return `${(speedNum / 1000000).toFixed(0)}M`;
    if (speedNum >= 1000) return `${(speedNum / 1000).toFixed(0)}K`;
    return `${speedNum}`;
  };

  // Función para obtener el nombre del dispositivo
  const getDeviceName = (deviceId) => {
    const device = devices.find(d => d.id === deviceId);
    return device ? device.device_name : `Device ${deviceId}`;
  };

  // Calcular estadísticas
  const activeInterfaces = interfaces.filter(i => i.estado_operativo === 'up' || i.estado_operativo === 'activo').length;
  const totalPages = Math.ceil(totalItems / itemsPerPage);
  const startItem = (currentPage - 1) * itemsPerPage + 1;
  const endItem = Math.min(currentPage * itemsPerPage, totalItems);

  return (
    <div className="interfaces-table-container">
      {/* Header con título y estadísticas */}
      <div className="table-header">
        <div className="header-title">
          <h2>🔌 Interfaces de Red</h2>
          <p>Monitoreo y gestión de interfaces en tiempo real</p>
        </div>
        <div className="header-stats">
          <div className="stat-card">
            <span className="stat-number">{totalItems}</span>
            <span className="stat-label">Total Interfaces</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{activeInterfaces}</span>
            <span className="stat-label">Activas</span>
          </div>
        </div>
      </div>

      {/* Filtros */}
      <div className="filters-section">
        <div className="filters-grid">
          <input
            type="text"
            placeholder="🔍 Buscar interfaz..."
            value={filters.search}
            onChange={(e) => handleFilterChange('search', e.target.value)}
            className="filter-input"
          />
          
          <select
            value={filters.interface_type}
            onChange={(e) => handleFilterChange('interface_type', e.target.value)}
            className="filter-select"
          >
            <option value="">Todos los tipos</option>
            <option value="ethernet">Ethernet</option>
            <option value="fiber">Fiber</option>
            <option value="wifi">WiFi</option>
            <option value="serial">Serial</option>
            <option value="loopback">Loopback</option>
            <option value="vlan">VLAN</option>
          </select>

          <select
            value={filters.dispositivo_id}
            onChange={(e) => handleFilterChange('dispositivo_id', e.target.value)}
            className="filter-select"
          >
            <option value="">Todos los dispositivos</option>
            {devices.map(device => (
              <option key={device.id} value={device.id}>
                {device.device_name}
              </option>
            ))}
          </select>

          <select
            value={filters.estado_operativo}
            onChange={(e) => handleFilterChange('estado_operativo', e.target.value)}
            className="filter-select"
          >
            <option value="">Todos los estados</option>
            <option value="up">Up</option>
            <option value="down">Down</option>
            <option value="testing">Testing</option>
          </select>

          <select
            value={filters.estado_administrativo}
            onChange={(e) => handleFilterChange('estado_administrativo', e.target.value)}
            className="filter-select"
          >
            <option value="">Estado Admin</option>
            <option value="enabled">Enabled</option>
            <option value="disabled">Disabled</option>
          </select>

          <button 
            onClick={() => {
              setFilters({
                search: '',
                interface_type: '',
                estado_administrativo: '',
                estado_operativo: '',
                dispositivo_id: '',
                velocidad: ''
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
          Mostrando {startItem} - {endItem} de {totalItems} interfaces
        </div>
      </div>

      {/* Tabla */}
      <div className="table-wrapper">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Cargando interfaces...</p>
          </div>
        ) : error ? (
          <div className="error-container">
            <p>❌ {error}</p>
            <button onClick={loadInterfaces} className="btn-retry">
              🔄 Reintentar
            </button>
          </div>
        ) : (
          <table className="interfaces-table">
            <thead>
              <tr>
                <th onClick={() => handleSort('interface_name')} className="sortable">
                  Interfaz {sortField === 'interface_name' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th onClick={() => handleSort('interface_type')} className="sortable">
                  Tipo {sortField === 'interface_type' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>Dispositivo</th>
                <th>Estado Operativo</th>
                <th>Estado Admin</th>
                <th onClick={() => handleSort('velocidad')} className="sortable">
                  Velocidad {sortField === 'velocidad' && (sortDirection === 'asc' ? '↑' : '↓')}
                </th>
                <th>MTU</th>
                <th>VLAN</th>
                <th>Tráfico</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {interfaces.map((interfaceItem) => (
                <tr key={interfaceItem.id} className="interface-row">
                  <td className="interface-name">
                    <strong>{interfaceItem.interface_name}</strong>
                    <small>{interfaceItem.descripcion}</small>
                  </td>
                  <td>
                    <span className={`type-badge type-${interfaceItem.interface_type}`}>
                      {interfaceItem.interface_type}
                    </span>
                  </td>
                  <td className="device-name">
                    {getDeviceName(interfaceItem.dispositivo_id)}
                  </td>
                  <td>
                    <span className={`status-badge ${getStatusClass(interfaceItem.estado_operativo)}`}>
                      {getStatusIcon(interfaceItem.estado_operativo)} {interfaceItem.estado_operativo}
                    </span>
                  </td>
                  <td>
                    <span className={`status-badge ${getStatusClass(interfaceItem.estado_administrativo)}`}>
                      {getStatusIcon(interfaceItem.estado_administrativo)} {interfaceItem.estado_administrativo}
                    </span>
                  </td>
                  <td className="speed">
                    {formatSpeed(interfaceItem.velocidad)}
                    {interfaceItem.velocidad && <small>bps</small>}
                  </td>
                  <td className="mtu">{interfaceItem.mtu || 'N/A'}</td>
                  <td className="vlan">{interfaceItem.vlan_id || '-'}</td>
                  <td className="traffic">
                    <div className="traffic-info">
                      <div className="traffic-item">
                        ⬇️ {formatSpeed(interfaceItem.bytes_in || 0)}B
                      </div>
                      <div className="traffic-item">
                        ⬆️ {formatSpeed(interfaceItem.bytes_out || 0)}B
                      </div>
                    </div>
                  </td>
                  <td className="actions">
                    <button
                      onClick={() => handleInterfaceDetails(interfaceItem)}
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

      {/* Modal de detalles de la interfaz */}
      {showInterfaceModal && selectedInterface && (
        <div className="modal-overlay" onClick={() => setShowInterfaceModal(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>🔌 Detalles de la Interfaz</h3>
              <button 
                onClick={() => setShowInterfaceModal(false)}
                className="btn-close"
              >
                ✕
              </button>
            </div>
            
            <div className="modal-body">
              <div className="interface-info-grid">
                <div className="info-section">
                  <h4>Información General</h4>
                  <div className="info-item">
                    <strong>Nombre:</strong> {selectedInterface.interface_name}
                  </div>
                  <div className="info-item">
                    <strong>Tipo:</strong> {selectedInterface.interface_type}
                  </div>
                  <div className="info-item">
                    <strong>Dispositivo:</strong> {getDeviceName(selectedInterface.dispositivo_id)}
                  </div>
                  <div className="info-item">
                    <strong>Descripción:</strong> {selectedInterface.descripcion || 'Sin descripción'}
                  </div>
                </div>

                <div className="info-section">
                  <h4>Estado y Configuración</h4>
                  <div className="info-item">
                    <strong>Estado Operativo:</strong>
                    <span className={`status-badge ${getStatusClass(selectedInterface.estado_operativo)}`}>
                      {getStatusIcon(selectedInterface.estado_operativo)} {selectedInterface.estado_operativo}
                    </span>
                  </div>
                  <div className="info-item">
                    <strong>Estado Admin:</strong>
                    <span className={`status-badge ${getStatusClass(selectedInterface.estado_administrativo)}`}>
                      {getStatusIcon(selectedInterface.estado_administrativo)} {selectedInterface.estado_administrativo}
                    </span>
                  </div>
                  <div className="info-item">
                    <strong>Velocidad:</strong> {formatSpeed(selectedInterface.velocidad)} bps
                  </div>
                  <div className="info-item">
                    <strong>MTU:</strong> {selectedInterface.mtu || 'N/A'}
                  </div>
                  <div className="info-item">
                    <strong>VLAN:</strong> {selectedInterface.vlan_id || 'No configurada'}
                  </div>
                </div>
              </div>

              <div className="traffic-section">
                <h4>Estadísticas de Tráfico</h4>
                <div className="traffic-stats-grid">
                  <div className="traffic-stat">
                    <div className="stat-icon">⬇️</div>
                    <div className="stat-content">
                      <div className="stat-value">{formatSpeed(selectedInterface.bytes_in || 0)}B</div>
                      <div className="stat-label">Bytes Recibidos</div>
                    </div>
                  </div>
                  <div className="traffic-stat">
                    <div className="stat-icon">⬆️</div>
                    <div className="stat-content">
                      <div className="stat-value">{formatSpeed(selectedInterface.bytes_out || 0)}B</div>
                      <div className="stat-label">Bytes Enviados</div>
                    </div>
                  </div>
                  <div className="traffic-stat">
                    <div className="stat-icon">📊</div>
                    <div className="stat-content">
                      <div className="stat-value">{selectedInterface.paquetes_in || 0}</div>
                      <div className="stat-label">Paquetes In</div>
                    </div>
                  </div>
                  <div className="traffic-stat">
                    <div className="stat-icon">📈</div>
                    <div className="stat-content">
                      <div className="stat-value">{selectedInterface.paquetes_out || 0}</div>
                      <div className="stat-label">Paquetes Out</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Estilos CSS (reutilizando muchos de DevicesTable con algunas modificaciones específicas) */}
      <style>{`
        .interfaces-table-container {
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

        .interfaces-table {
          width: 100%;
          border-collapse: collapse;
          background: white;
        }

        .interfaces-table th {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 1rem 0.75rem;
          text-align: left;
          font-weight: 600;
          position: sticky;
          top: 0;
          z-index: 10;
          white-space: nowrap;
        }

        .interfaces-table th.sortable {
          cursor: pointer;
          user-select: none;
          transition: background-color 0.2s;
        }

        .interfaces-table th.sortable:hover {
          background: rgba(102, 126, 234, 0.9);
        }

        .interfaces-table td {
          padding: 0.75rem;
          border-bottom: 1px solid #f0f0f0;
          vertical-align: top;
        }

        .interface-row:hover {
          background: #f8f9fa;
        }

        .interface-name {
          min-width: 150px;
        }

        .interface-name strong {
          display: block;
          margin-bottom: 0.25rem;
        }

        .interface-name small {
          color: #666;
          font-size: 0.8rem;
        }

        .device-name {
          font-size: 0.9rem;
          color: #555;
        }

        .type-badge {
          display: inline-block;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          font-size: 0.8rem;
          font-weight: 500;
          text-transform: capitalize;
        }

        .type-ethernet { background: #e3f2fd; color: #1976d2; }
        .type-fiber { background: #f3e5f5; color: #7b1fa2; }
        .type-wifi { background: #e8f5e8; color: #388e3c; }
        .type-serial { background: #fff3e0; color: #f57c00; }
        .type-loopback { background: #ffebee; color: #d32f2f; }
        .type-vlan { background: #e1f5fe; color: #0277bd; }

        .speed {
          font-family: 'Courier New', monospace;
          font-size: 0.9rem;
        }

        .speed small {
          display: block;
          font-size: 0.7rem;
          color: #666;
        }

        .mtu, .vlan {
          font-size: 0.9rem;
          color: #555;
        }

        .traffic {
          min-width: 120px;
        }

        .traffic-info {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
        }

        .traffic-item {
          font-size: 0.8rem;
          color: #555;
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
          max-width: 900px;
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

        .interface-info-grid {
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
          min-width: 140px;
          color: #555;
        }

        .traffic-section h4 {
          margin: 0 0 1rem 0;
          color: #333;
        }

        .traffic-stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 1rem;
        }

        .traffic-stat {
          background: #f8f9fa;
          padding: 1rem;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 1rem;
          border-left: 4px solid #667eea;
        }

        .stat-icon {
          font-size: 1.5rem;
        }

        .stat-content {
          flex: 1;
        }

        .stat-value {
          font-size: 1.2rem;
          font-weight: bold;
          color: #333;
        }

        .stat-label {
          font-size: 0.9rem;
          color: #666;
        }

        /* Responsive */
        @media (max-width: 768px) {
          .interfaces-table-container {
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

          .interfaces-table {
            font-size: 0.9rem;
          }

          .interfaces-table th,
          .interfaces-table td {
            padding: 0.5rem;
          }

          .interface-info-grid {
            grid-template-columns: 1fr;
            gap: 1rem;
          }

          .traffic-stats-grid {
            grid-template-columns: 1fr;
          }

          .modal-content {
            margin: 0.5rem;
          }
        }
      `}</style>
    </div>
  );
};

export default InterfacesTable;
