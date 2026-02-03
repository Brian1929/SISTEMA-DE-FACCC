import axios from 'axios';

const API_BASE_URL = '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos de timeout
});

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      error.message = 'Tiempo de espera agotado. Verifique que el servidor esté corriendo.';
    } else if (error.response) {
      // El servidor respondió con un código de error
      error.message = error.response.data?.message || error.response.data?.error || error.message;
    } else if (error.request) {
      // La petición se hizo pero no hubo respuesta
      error.message = 'No se pudo conectar con el servidor. Asegúrese de que el backend esté corriendo en http://localhost:5000';
    }
    return Promise.reject(error);
  }
);

// Configuración
export const getConfig = () => api.get('/configuracion');
export const updateConfig = (data) => api.post('/configuracion', data);

// Productos
export const getProductos = () => api.get('/productos');
export const createProducto = (data) => api.post('/productos', data);
export const updateProducto = (codigo, data) => api.put(`/productos/${codigo}`, data);
export const deleteProducto = (codigo) => api.delete(`/productos/${codigo}`);
export const getProducto = (codigo) => api.get(`/productos/${codigo}`);

// Facturas
export const getNumeroFactura = () => api.get('/facturas/numero');
export const createFactura = (data) => api.post('/facturas', data);
export const imprimirFactura = (data, responseType = 'blob') => {
  return api.post('/facturas/imprimir', data, {
    responseType: responseType,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};

// Formatos e Impresores
export const getFormatos = () => api.get('/formatos');
export const getImpresores = () => api.get('/impresores');

// Gestión de Facturas Históricas
export const getFacturas = () => api.get('/facturas');
export const getFacturaInfo = (numero) => api.get(`/facturas/${encodeURIComponent(numero)}`);
export const getEstadisticas = () => api.get('/facturas/estadisticas');

// Cotizaciones
export const getNumeroCotizacion = () => api.get('/cotizaciones/numero');
export const getCotizaciones = () => api.get('/cotizaciones');
export const createCotizacion = (data) => api.post('/cotizaciones', data);
export const getCotizacion = (numero) => api.get(`/cotizaciones/${encodeURIComponent(numero)}`);
export const imprimirCotizacion = (data, responseType = 'blob') => {
  return api.post('/cotizaciones/imprimir', data, {
    responseType: responseType,
    headers: {
      'Content-Type': 'application/json',
    },
  });
};
export const convertirCotizacion = (numero) => api.post('/cotizaciones/convertir', { numero });

export default api;

