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
    </div>
  );
};

export default InterfacesTable;
