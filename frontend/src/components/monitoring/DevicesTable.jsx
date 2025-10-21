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
    </div>
  );
};

export default DevicesTable;
