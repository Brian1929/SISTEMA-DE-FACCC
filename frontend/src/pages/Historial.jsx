import { useState, useEffect } from 'react';
import { getFacturas, imprimirFactura, getFacturaInfo } from '../services/api';
import './Historial.css';

function Historial() {
  const [facturas, setFacturas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState('');
  const [showPreview, setShowPreview] = useState(false);
  const [previewData, setPreviewData] = useState(null);
  const [previewNumero, setPreviewNumero] = useState('');

  useEffect(() => {
    loadFacturas();
  }, []);

  const loadFacturas = async () => {
    try {
      setLoading(true);
      const response = await getFacturas();
      if (response.data.success) {
        setFacturas(response.data.facturas);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error al cargar facturas:', err);
      setError('No se pudieron cargar las facturas guardadas.');
      setLoading(false);
    }
  };

  const descargarPDF = async (numero) => {
    try {
      const factura = facturas.find(f => f.numero === numero);
      const data = {
        numero,
        cliente: factura?.cliente || '',
        items: [], // El backend carga los items automáticamente si el número ya existe en facturas.json
        tipo_impresor: 'pdf',
        formato_papel: 'normal'
      };

      const response = await imprimirFactura(data);
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `factura_${numero}.pdf`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error al descargar PDF:', err);
      alert('Error al descargar el PDF de la factura.');
    }
  };

  const verVistaPrevia = async (numero) => {
    try {
      const response = await getFacturaInfo(numero);
      if (response.data.success) {
        setPreviewData(response.data.factura);
        setPreviewNumero(numero);
        setShowPreview(true);
      }
    } catch (err) {
      console.error('Error al obtener detalles de factura:', err);
      alert('Error al obtener los detalles de la factura.');
    }
  };

  const filteredFacturas = facturas.filter(f =>
    f.numero.toLowerCase().includes(search.toLowerCase()) ||
    f.cliente.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="container"><p>Cargando historial...</p></div>;
  if (error) return <div className="container"><p className="error">{error}</p></div>;

  return (
    <div className="historial-page">
      <div className="page-header">
        <h1>Historial de Facturas</h1>
        <div className="header-actions">
          <div className="search-container">
            <span className="search-icon">🔍</span>
            <input
              type="text"
              placeholder="Buscar por nombre o número..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="search-input"
            />
          </div>
          <button className="btn btn-primary" onClick={loadFacturas}>Actualizar</button>
        </div>
      </div>

      <div className="card">
        {facturas.length === 0 ? (
          <p>No hay facturas guardadas en el sistema.</p>
        ) : filteredFacturas.length === 0 ? (
          <p>No se encontraron facturas que coincidan con la búsqueda.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Número</th>
                  <th>Fecha</th>
                  <th>Cliente</th>
                  <th>Items</th>
                  <th>Total</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filteredFacturas.map((f) => (
                  <tr key={f.numero}>
                    <td>{f.numero}</td>
                    <td>{new Date(f.fecha).toLocaleString()}</td>
                    <td>{f.cliente}</td>
                    <td>{f.items_count}</td>
                    <td>${f.total.toFixed(2)}</td>
                    <td>
                      <div className="action-buttons">
                        <button className="btn btn-sm btn-info" onClick={() => verVistaPrevia(f.numero)}>
                          Ver
                        </button>
                        <button className="btn btn-sm btn-success" onClick={() => descargarPDF(f.numero)}>
                          PDF
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showPreview && (
        <div className="modal-overlay" onClick={() => setShowPreview(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Detalle de Factura - {previewData?.numero}</h3>
              <button className="close-btn" onClick={() => setShowPreview(false)}>&times;</button>
            </div>
            <div className="modal-body">
              {previewData && (
                <div className="preview-visual">
                  <div className="preview-section">
                    <div className="info-grid">
                      <div className="info-item">
                        <strong>Cliente:</strong> {previewData.cliente}
                      </div>
                      <div className="info-item">
                        <strong>Fecha:</strong> {new Date(previewData.fecha).toLocaleString()}
                      </div>
                      {previewData.notas && (
                        <div className="info-item full-width">
                          <strong>Notas:</strong> {previewData.notas}
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="preview-section">
                    <h4>Productos</h4>
                    <div className="table-container small-table">
                      <table>
                        <thead>
                          <tr>
                            <th>Código</th>
                            <th>Producto</th>
                            <th>Cant.</th>
                            <th>Precio</th>
                            <th>Subtotal</th>
                          </tr>
                        </thead>
                        <tbody>
                          {previewData.items.map((item, idx) => (
                            <tr key={idx}>
                              <td>{item.producto.codigo}</td>
                              <td>{item.producto.nombre}</td>
                              <td>{item.cantidad.toFixed(2)}</td>
                              <td>${item.producto.precio.toFixed(2)}</td>
                              <td>${item.subtotal.toFixed(2)}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>

                  <div className="preview-totals">
                    <div className="total-row">
                      <span>Subtotal:</span>
                      <span>${previewData.subtotal.toFixed(2)}</span>
                    </div>
                    {previewData.impuesto > 0 && (
                      <div className="total-row">
                        <span>Impuesto:</span>
                        <span>${previewData.impuesto_monto?.toFixed(2) || (previewData.subtotal * (previewData.impuesto / 100)).toFixed(2)}</span>
                      </div>
                    )}
                    <div className="total-row total-final">
                      <span>TOTAL:</span>
                      <span>${previewData.total.toFixed(2)}</span>
                    </div>
                  </div>
                </div>
              )}
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowPreview(false)}>Cerrar</button>
              <button className="btn btn-success" onClick={() => {
                setShowPreview(false);
                descargarPDF(previewNumero);
              }}>Descargar PDF</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Historial;
