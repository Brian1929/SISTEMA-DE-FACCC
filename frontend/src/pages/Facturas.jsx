import { useState, useEffect } from 'react';
import { getProductos, getNumeroFactura, createFactura, imprimirFactura, getCotizacion } from '../services/api';
import Modal from '../components/Modal';
import './Facturas.css';

function Facturas() {
  const [productos, setProductos] = useState([]);
  const [items, setItems] = useState([]);
  const [numeroFactura, setNumeroFactura] = useState('');
  const [cliente, setCliente] = useState('');
  const [impuesto, setImpuesto] = useState(0);
  const [notas, setNotas] = useState('');
  const [productoSeleccionado, setProductoSeleccionado] = useState('');
  const [busquedaProducto, setBusquedaProducto] = useState('');
  const [cotizacionBusqueda, setCotizacionBusqueda] = useState('');
  const [cotizacionOrigen, setCotizacionOrigen] = useState(null); // Para guardar el numero de cot cargada
  const [mostrarResultados, setMostrarResultados] = useState(false);
  const [cantidad, setCantidad] = useState(1);
  const [showPreview, setShowPreview] = useState(false);
  const [previewContent, setPreviewContent] = useState('');

  useEffect(() => {
    loadProductos();
    loadNumeroFactura();
  }, []);

  const loadProductos = async () => {
    try {
      const response = await getProductos();
      setProductos(response.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
    }
  };

  const loadNumeroFactura = async () => {
    try {
      const response = await getNumeroFactura();
      setNumeroFactura(response.data.numero);
    } catch (error) {
      console.error('Error al cargar número de factura:', error);
    }
  };

  const handleCargarCotizacion = async () => {
    if (!cotizacionBusqueda) return;
    try {
      const res = await getCotizacion(cotizacionBusqueda);
      if (res.data.success) {
        const cot = res.data.cotizacion;
        setCliente(cot.cliente);
        setNotas(cot.notas || '');
        setCotizacionOrigen(cot.numero); // Guardar referencia
        // Mapear items de cotización a items de factura (asegurando precios actuales si se desea, o manteniendo los de la cot)
        // Aquí mantenemos los de la cotización
        const nuevosItems = cot.items.map(i => ({
          codigo: i.producto.codigo,
          nombre: i.producto.nombre, // Asumiendo que el objeto producto viene populado
          precio: i.producto.precio,
          cantidad: i.cantidad,
          subtotal: i.producto.precio * i.cantidad
        }));
        setItems(nuevosItems);
        alert(`✓ Cotización ${cot.numero} cargada.`);
      }
    } catch (error) {
      alert('Error al cargar cotización: ' + (error.response?.data?.message || error.message));
    }
  };

  const agregarItem = () => {
    const producto = productos.find(p => p.codigo === productoSeleccionado);
    if (!producto) {
      alert('Seleccione un producto');
      return;
    }
    if (cantidad <= 0) {
      alert('La cantidad debe ser mayor a cero');
      return;
    }

    if (producto.stock < cantidad) {
      alert(`⚠️ Stock insuficiente. Solo quedan ${producto.stock} unidades disponibles.`);
      return;
    }

    const subtotal = producto.precio * cantidad;
    const nuevoItem = {
      codigo: producto.codigo,
      nombre: producto.nombre,
      precio: producto.precio,
      cantidad: parseFloat(cantidad),
      subtotal: subtotal
    };

    setItems([...items, nuevoItem]);
    setProductoSeleccionado('');
    setBusquedaProducto('');
    setCantidad(1);
  };

  const eliminarItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  const calcularSubtotal = () => {
    return items.reduce((sum, item) => sum + item.subtotal, 0);
  };

  const calcularImpuesto = () => {
    return 0;
  };

  const calcularTotal = () => {
    return calcularSubtotal() + calcularImpuesto();
  };

  const limpiarFactura = () => {
    if (window.confirm('¿Está seguro de limpiar la factura? Se generará un nuevo número de factura.')) {
      setItems([]);
      setCliente('');
      setImpuesto(0);
      setNotas('');
      setCotizacionOrigen(null);
      setCotizacionBusqueda('');
      loadNumeroFactura();
    }
  };

  const vistaPrevia = async () => {
    if (!numeroFactura || !cliente) {
      alert('Complete el número de factura y el cliente');
      return;
    }
    if (items.length === 0) {
      alert('Agregue al menos un producto');
      return;
    }

    try {
      const data = {
        numero: numeroFactura,
        cliente,
        impuesto,
        notas,
        es_vista_previa: true,
        items: items.map(item => ({
          codigo: item.codigo,
          cantidad: item.cantidad
        }))
      };

      const response = await createFactura(data);
      setPreviewContent(response.data.factura.vista_previa);
      setShowPreview(true);
    } catch (error) {
      alert('Error: ' + (error.response?.data?.message || error.message));
    }
  };

  const generarPDF = async () => {
    if (!numeroFactura || !cliente) {
      alert('Complete el número de factura y el cliente');
      return;
    }
    if (items.length === 0) {
      alert('Agregue al menos un producto');
      return;
    }

    try {
      const data = {
        numero: numeroFactura,
        cliente,
        impuesto,
        notas,
        origen_cotizacion: cotizacionOrigen, // Enviar origen
        tipo_impresor: 'pdf',
        formato_papel: 'normal',
        items: items.map(item => ({
          codigo: item.codigo,
          cantidad: item.cantidad
        }))
      };

      const response = await imprimirFactura(data);

      // Verificar el tipo de contenido de la respuesta
      const contentType = response.headers['content-type'] || '';

      if (contentType.includes('application/pdf') || response.data instanceof Blob) {
        // Es un PDF - descargarlo
        const blob = response.data instanceof Blob ? response.data : new Blob([response.data], { type: 'application/pdf' });
        const url = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `factura_${numeroFactura}.pdf`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);
        console.log('✓ PDF descargado exitosamente');
      } else {
        // Es un error JSON
        let errorMessage = 'Error al generar PDF';
        try {
          if (response.data instanceof Blob) {
            const text = await response.data.text();
            const errorData = JSON.parse(text);
            errorMessage = errorData.message || errorMessage;
          } else if (typeof response.data === 'object') {
            errorMessage = response.data.message || errorMessage;
          }
        } catch (e) {
          console.error('Error al parsear respuesta:', e);
        }
        alert('✗ Error: ' + errorMessage);
      }
    } catch (error) {
      alert('Error: ' + (error.response?.data?.message || error.message));
    }
  };

  const guardarFactura = async () => {
    if (!numeroFactura || !cliente) {
      alert('Complete el número de factura y el cliente');
      return;
    }
    if (items.length === 0) {
      alert('Agregue al menos un producto');
      return;
    }

    try {
      const data = {
        numero: numeroFactura,
        cliente,
        impuesto,
        notas,
        origen_cotizacion: cotizacionOrigen, // Enviar origen
        items: items.map(item => ({
          codigo: item.codigo,
          cantidad: item.cantidad
        }))
      };

      const response = await createFactura(data);
      if (response.data.success) {
        alert('✓ Factura guardada exitosamente en el sistema');
        limpiarDespuesDeGuardar();
      }
    } catch (error) {
      alert('Error al guardar: ' + (error.response?.data?.message || error.message));
    }
  };

  const limpiarDespuesDeGuardar = () => {
    setItems([]);
    setCliente('');
    setImpuesto(0);
    setNotas('');
    setCotizacionOrigen(null);
    setCotizacionBusqueda('');
    loadNumeroFactura();
  };

  return (
    <div className="facturas-page">
      <div className="page-header">
        <h1>Crear Factura</h1>
      </div>

      <div className="invoice-container">
        <div className="compact-layout">
          <div className="card compact-card">
            <h3>Información Cliente</h3>
            <div className="form-group compact">
              <label>Cliente *</label>
              <input
                type="text"
                value={cliente}
                onChange={(e) => setCliente(e.target.value)}
                required
                placeholder="Nombre del cliente"
              />
            </div>
            <div className="form-row compact">
              <div className="form-group compact">
                <label>Número</label>
                <input
                  type="text"
                  value={numeroFactura}
                  readOnly
                  className="read-only-input"
                />
              </div>
              <div className="form-group compact" style={{ marginLeft: '10px' }}>
                <label>Cargar Cotización</label>
                <div style={{ display: 'flex', gap: '5px' }}>
                  <input
                    type="text"
                    placeholder="COT-XXXX"
                    value={cotizacionBusqueda}
                    onChange={(e) => setCotizacionBusqueda(e.target.value)}
                    style={{ width: '120px' }}
                  />
                  <button className="btn btn-sm btn-info" onClick={handleCargarCotizacion}>⤵</button>
                </div>
              </div>
            </div>
          </div>

          <div className="card compact-card">
            <h3>Agregar Producto</h3>
            <div className="form-group compact search-container">
              <label>Buscar Producto (Nombre o Código)</label>
              <div className="search-input-wrapper">
                <input
                  type="text"
                  placeholder="Escriba código o nombre..."
                  value={busquedaProducto}
                  onChange={(e) => {
                    setBusquedaProducto(e.target.value);
                    setMostrarResultados(true);
                  }}
                  onFocus={() => setMostrarResultados(true)}
                />
                {mostrarResultados && busquedaProducto && (
                  <div className="search-results-dropdown">
                    {productos
                      .filter(p =>
                        p.nombre.toLowerCase().includes(busquedaProducto.toLowerCase()) ||
                        p.codigo.toLowerCase().includes(busquedaProducto.toLowerCase())
                      )
                      .slice(0, 8)
                      .map(p => (
                        <div
                          key={p.codigo}
                          className="search-result-item"
                          onClick={() => {
                            setProductoSeleccionado(p.codigo);
                            setBusquedaProducto(`${p.nombre} (${p.codigo})`);
                            setMostrarResultados(false);
                          }}
                        >
                          <div className="res-info">
                            <span className="res-name">{p.nombre}</span>
                            <span className="res-code">{p.codigo}</span>
                          </div>
                          <div className="res-meta">
                            <span className="res-price">${parseFloat(p.price || p.precio).toFixed(2)}</span>
                            <span className={`res-stock ${parseFloat(p.stock) <= 5 ? 'low' : ''}`}>Stock: {p.stock}</span>
                          </div>
                        </div>
                      ))
                    }
                  </div>
                )}
              </div>
            </div>
            {productoSeleccionado && (
              <div className="stock-hint" style={{ fontSize: '0.85rem', marginBottom: '1rem', color: (productos.find(p => p.codigo === productoSeleccionado)?.stock || 0) <= 5 ? '#e74c3c' : '#27ae60' }}>
                Stock disponible: <strong>{productos.find(p => p.codigo === productoSeleccionado)?.stock || 0}</strong>
              </div>
            )}
            <div className="form-row compact">
              <div className="form-group compact">
                <label>Cant.</label>
                <input
                  type="number"
                  step="0.01"
                  value={cantidad}
                  onChange={(e) => setCantidad(parseFloat(e.target.value) || 1)}
                />
              </div>
              <div className="form-group compact action-btn-container">
                <button className="btn btn-primary btn-block" onClick={agregarItem}>
                  +
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="card compact-card items-card">
          <div className="items-header">
            <h3>Items de la Factura</h3>
            <div className="notas-inline">
              <label>Notas:</label>
              <input
                type="text"
                value={notas}
                onChange={(e) => setNotas(e.target.value)}
                placeholder="Notas opcionales..."
              />
            </div>
          </div>

          <div className="table-container compact-table">
            <table>
              <thead>
                <tr>
                  <th>Producto</th>
                  <th>Cant.</th>
                  <th>Precio</th>
                  <th>Subtotal</th>
                  <th className="text-center">X</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item, index) => (
                  <tr key={index}>
                    <td><strong>{item.codigo}</strong> - {item.nombre}</td>
                    <td>{item.cantidad.toFixed(2)}</td>
                    <td>${item.precio.toFixed(2)}</td>
                    <td>${item.subtotal.toFixed(2)}</td>
                    <td className="text-center">
                      <button className="btn-icon btn-danger" onClick={() => eliminarItem(index)}>×</button>
                    </td>
                  </tr>
                ))}
                {items.length === 0 && (
                  <tr>
                    <td colSpan="5" className="empty-row">No hay productos agregados</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>

          <div className="footer-container">
            <div className="invoice-totals compact-totals">
              <div className="total-row">
                <span>Subtotal:</span>
                <span>${calcularSubtotal().toFixed(2)}</span>
              </div>
              <div className="total-row total-final">
                <span>Total:</span>
                <span>${calcularTotal().toFixed(2)}</span>
              </div>
            </div>

            <div className="action-buttons-group">
              <button className="btn btn-secondary btn-sm" onClick={limpiarFactura}>Limpiar</button>
              <button className="btn btn-info btn-sm" onClick={vistaPrevia}>Vista Previa</button>
              <button className="btn btn-primary btn-sm" onClick={guardarFactura}>Guardar</button>
              <button className="btn btn-success btn-sm" onClick={generarPDF}>Generar PDF</button>
            </div>
          </div>
        </div>
      </div>

      <Modal show={showPreview} onClose={() => setShowPreview(false)} title="Vista Previa de la Factura">
        <pre className="invoice-preview">{previewContent}</pre>
      </Modal>
    </div>
  );
}

export default Facturas;

