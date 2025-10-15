/**
 * Servicio de Monitoreo
 * Maneja todas las peticiones relacionadas con el módulo de monitoreo
 */
import { apiClient } from './authService';

/**
 * Obtiene todos los dispositivos con filtros opcionales
 * @param {Object} filters - Filtros a aplicar
 * @param {number} skip - Número de registros a saltar (paginación)
 * @param {number} limit - Límite de registros a obtener
 * @returns {Promise<Object>} Lista de dispositivos
 */
export const getDevices = async (filters = {}, skip = 0, limit = 100) => {
  try {
    const params = new URLSearchParams();
    
    // Agregar parámetros de paginación
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    // Agregar filtros si existen
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });

    const response = await apiClient.get(`/monitoreo/dispositivos/?${params.toString()}`);
    
    return {
      success: true,
      data: response.data,
      total: response.headers['x-total-count'] ? parseInt(response.headers['x-total-count']) : response.data.length
    };
  } catch (error) {
    console.error('Error obteniendo dispositivos:', error);
    return {
      success: false,
      message: 'Error al obtener los dispositivos',
      error: error.response?.data?.detail || error.message,
      data: []
    };
  }
};

/**
 * Obtiene un dispositivo específico por ID
 * @param {number} deviceId - ID del dispositivo
 * @returns {Promise<Object>} Datos del dispositivo
 */
export const getDeviceById = async (deviceId) => {
  try {
    const response = await apiClient.get(`/monitoreo/dispositivos/${deviceId}`);
    
    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    console.error('Error obteniendo dispositivo:', error);
    return {
      success: false,
      message: 'Error al obtener el dispositivo',
      error: error.response?.data?.detail || error.message,
      data: null
    };
  }
};

/**
 * Obtiene las interfaces con filtros opcionales
 * @param {Object} filters - Filtros a aplicar
 * @param {number} skip - Número de registros a saltar (paginación)
 * @param {number} limit - Límite de registros a obtener
 * @returns {Promise<Object>} Lista de interfaces
 */
export const getInterfaces = async (filters = {}, skip = 0, limit = 100) => {
  try {
    const params = new URLSearchParams();
    
    // Agregar parámetros de paginación
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    
    // Agregar filtros si existen
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null && value !== '') {
        params.append(key, value.toString());
      }
    });

    const response = await apiClient.get(`/monitoreo/interfaces/?${params.toString()}`);
    
    return {
      success: true,
      data: response.data,
      total: response.headers['x-total-count'] ? parseInt(response.headers['x-total-count']) : response.data.length
    };
  } catch (error) {
    console.error('Error obteniendo interfaces:', error);
    return {
      success: false,
      message: 'Error al obtener las interfaces',
      error: error.response?.data?.detail || error.message,
      data: []
    };
  }
};

/**
 * Obtiene una interfaz específica por ID
 * @param {number} interfaceId - ID de la interfaz
 * @returns {Promise<Object>} Datos de la interfaz
 */
export const getInterfaceById = async (interfaceId) => {
  try {
    const response = await apiClient.get(`/monitoreo/interfaces/${interfaceId}`);
    
    return {
      success: true,
      data: response.data
    };
  } catch (error) {
    console.error('Error obteniendo interfaz:', error);
    return {
      success: false,
      message: 'Error al obtener la interfaz',
      error: error.response?.data?.detail || error.message,
      data: null
    };
  }
};

/**
 * Obtiene las interfaces de un dispositivo específico
 * @param {number} deviceId - ID del dispositivo
 * @param {number} skip - Número de registros a saltar
 * @param {number} limit - Límite de registros
 * @returns {Promise<Object>} Lista de interfaces del dispositivo
 */
export const getDeviceInterfaces = async (deviceId, skip = 0, limit = 50) => {
  try {
    const response = await apiClient.get(`/monitoreo/dispositivos/${deviceId}/interfaces`, {
      params: { skip, limit }
    });
    
    return {
      success: true,
      data: response.data,
      total: response.headers['x-total-count'] ? parseInt(response.headers['x-total-count']) : response.data.length
    };
  } catch (error) {
    console.error('Error obteniendo interfaces del dispositivo:', error);
    return {
      success: false,
      message: 'Error al obtener las interfaces del dispositivo',
      error: error.response?.data?.detail || error.message,
      data: []
    };
  }
};

/**
 * Obtiene estadísticas generales del monitoreo
 * @returns {Promise<Object>} Estadísticas del sistema
 */
export const getMonitoringStats = async () => {
  try {
    const [devicesResult, interfacesResult] = await Promise.all([
      getDevices({}, 0, 1), // Solo para obtener el total
      getInterfaces({}, 0, 1) // Solo para obtener el total
    ]);

    // Calcular estadísticas adicionales
    const totalDevices = devicesResult.total || 0;
    const totalInterfaces = interfacesResult.total || 0;

    return {
      success: true,
      data: {
        totalDevices,
        totalInterfaces,
        avgInterfacesPerDevice: totalDevices > 0 ? (totalInterfaces / totalDevices).toFixed(2) : 0
      }
    };
  } catch (error) {
    console.error('Error obteniendo estadísticas:', error);
    return {
      success: false,
      message: 'Error al obtener las estadísticas',
      error: error.message,
      data: {
        totalDevices: 0,
        totalInterfaces: 0,
        avgInterfacesPerDevice: 0
      }
    };
  }
};

export default {
  getDevices,
  getDeviceById,
  getInterfaces,
  getInterfaceById,
  getDeviceInterfaces,
  getMonitoringStats
};
