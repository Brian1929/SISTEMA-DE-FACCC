
import React, { useState, useEffect } from 'react';
import {
    getNumeroCotizacion,
    getProductos,
    createCotizacion,
    imprimirCotizacion,
    getCotizaciones,
    convertirCotizacion
} from '../services/api';
import './Facturas.css'; // Reutilizamos estilos

const Cotizaciones = () => {
    const [numeroCotizacion, setNumeroCotizacion] = useState('');
    const [cliente, setCliente] = useState('');
    const [items, setItems] = useState([]);
    const [productos, setProductos] = useState([]);
    const [busqueda, setBusqueda] = useState('');
    const [notas, setNotas] = useState('');
    const [loading, setLoading] = useState(false);
    const [historialCotizaciones, setHistorialCotizaciones] = useState([]);
    const [vista, setVista] = useState('nueva'); // 'nueva' o 'listado'

    useEffect(() => {
        cargarDatos();
    }, []);

    const cargarDatos = async () => {
        try {
            const [numRes, prodRes, cotsRes] = await Promise.all([
                getNumeroCotizacion(),
                getProductos(),
                getCotizaciones()
            ]);
            setNumeroCotizacion(numRes.data.numero);
            setProductos(prodRes.data);
            setHistorialCotizaciones(cotsRes.data);
        } catch (error) {
            console.error('Error al cargar datos:', error);
        }
    };

    const agregarProducto = (producto) => {
        const existe = items.find(item => item.codigo === producto.codigo);
        if (existe) {
            setItems(items.map(item =>
                item.codigo === producto.codigo
                    ? { ...item, cantidad: item.cantidad + 1 }
                    : item
            ));
        } else {
            setItems([...items, { ...producto, cantidad: 1 }]);
        }
        setBusqueda('');
    };

    const eliminarItem = (codigo) => {
        setItems(items.filter(item => item.codigo !== codigo));
    };

    const calcularTotal = () => {
        const subtotal = items.reduce((acc, item) => acc + (item.precio * item.cantidad), 0);
        return subtotal;
    };

    const handleGuardar = async () => {
        if (!cliente || items.length === 0) {
            alert('Favor completar cliente y agregar al menos un producto');
            return;
        }

        setLoading(true);
        try {
            const data = {
                numero: numeroCotizacion,
                cliente,
                notas,
                items: items.map(i => ({ codigo: i.codigo, cantidad: i.cantidad })),
                impuesto: 0
            };

            await createCotizacion(data);
            alert('✓ Cotización guardada con éxito');
            limpiarFormulario();
            cargarDatos();
            setVista('listado');
        } catch (error) {
            alert('Error al guardar cotización: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const descargarPDF = async (cot) => {
        try {
            const response = await imprimirCotizacion(cot);
            const blob = new Blob([response.data], { type: 'application/pdf' });
            const url = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `cotizacion_${cot.numero}.pdf`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            window.URL.revokeObjectURL(url);
        } catch (error) {
            alert('Error al generar PDF: ' + error.message);
        }
    };

    const handleConvertir = async (cot) => {
        if (!window.confirm(`¿Convertir cotización ${cot.numero} en Factura oficial? Esto descontará el stock.`)) return;

        try {
            const res = await convertirCotizacion(cot.numero);
            alert(`✓ ${res.data.message}`);
            cargarDatos();
        } catch (error) {
            alert('Error al convertir: ' + error.message);
        }
    };

    const limpiarFormulario = () => {
        setCliente('');
        setItems([]);
        setNotas('');
    };

    const productosFiltrados = busqueda
        ? productos.filter(p =>
            p.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
            p.codigo.toLowerCase().includes(busqueda.toLowerCase())
        )
        : [];

    return (
        <div className="facturas-page">
            <div className="page-header">
                <h2>📑 Módulo de Cotizaciones</h2>
                <div className="tabs">
                    <button className={`tab ${vista === 'nueva' ? 'active' : ''}`} onClick={() => setVista('nueva')}>Nueva Cotización</button>
                    <button className={`tab ${vista === 'listado' ? 'active' : ''}`} onClick={() => setVista('listado')}>Historial</button>
                </div>
            </div>

            {vista === 'nueva' ? (
                <div className="factura-grid">
                    <div className="card form-card">
                        <h3>Crear Presupuesto <span className="badge-cot">{numeroCotizacion}</span></h3>

                        <div className="form-group">
                            <label>Cliente</label>
                            <input
                                type="text"
                                className="form-control"
                                value={cliente}
                                onChange={(e) => setCliente(e.target.value)}
                                placeholder="Nombre del cliente"
                            />
                        </div>

                        <div className="form-group search-container">
                            <label>Buscar Productos</label>
                            <input
                                type="text"
                                className="form-control"
                                value={busqueda}
                                onChange={(e) => setBusqueda(e.target.value)}
                                placeholder="Escribe nombre o código..."
                            />
                            {productosFiltrados.length > 0 && (
                                <div className="search-results">
                                    {productosFiltrados.map(p => (
                                        <div key={p.codigo} className="search-item" onClick={() => agregarProducto(p)}>
                                            <span>{p.nombre} ({p.codigo})</span>
                                            <strong>${p.precio.toFixed(2)}</strong>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>

                        <div className="form-group">
                            <label>Notas Adicionales</label>
                            <textarea
                                className="form-control"
                                rows="3"
                                value={notas}
                                onChange={(e) => setNotas(e.target.value)}
                                placeholder="Términos de pago, validez de oferta, etc."
                            />
                        </div>
                    </div>

                    <div className="card summary-card">
                        <h3>Resumen</h3>
                        <div className="items-list">
                            {items.length === 0 ? (
                                <p className="empty-msg">No hay productos agregados</p>
                            ) : (
                                items.map(item => (
                                    <div key={item.codigo} className="item-row">
                                        <div className="item-info">
                                            <span className="item-name">{item.name || item.nombre}</span>
                                            <small>${item.precio.toFixed(2)} x {item.cantidad}</small>
                                        </div>
                                        <div className="item-actions">
                                            <span className="item-subtotal">${(item.precio * item.cantidad).toFixed(2)}</span>
                                            <button onClick={() => eliminarItem(item.codigo)} className="btn-delete">×</button>
                                        </div>
                                    </div>
                                ))
                            )}
                        </div>
                        <div className="totals">
                            <div className="total-row">
                                <span>TOTAL</span>
                                <strong>${calcularTotal().toFixed(2)}</strong>
                            </div>
                        </div>
                        <button
                            className="btn btn-primary btn-block"
                            onClick={handleGuardar}
                            disabled={loading || items.length === 0}
                        >
                            {loading ? 'Guardando...' : '💾 Guardar Cotización'}
                        </button>
                    </div>
                </div>
            ) : (
                <div className="card">
                    <h3>Historial de Cotizaciones</h3>
                    <table className="table">
                        <thead>
                            <tr>
                                <th>Número</th>
                                <th>Cliente</th>
                                <th>Fecha</th>
                                <th>Estado</th>
                                <th>Total</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {historialCotizaciones.map(cot => (
                                <tr key={cot.numero}>
                                    <td>{cot.numero}</td>
                                    <td>{cot.cliente}</td>
                                    <td>{new Date(cot.fecha).toLocaleDateString()}</td>
                                    <td><span className={`status-${cot.estado.toLowerCase()}`}>{cot.estado}</span></td>
                                    <td>${cot.total.toFixed(2)}</td>
                                    <td>
                                        <div className="action-buttons-group">
                                            <button className="btn btn-sm btn-secondary" onClick={() => descargarPDF(cot)}>📄 PDF</button>
                                            {cot.estado !== 'Facturada' && (
                                                <button
                                                    className="btn btn-sm btn-success"
                                                    style={{ backgroundColor: '#2ecc71', color: 'white' }}
                                                    onClick={() => handleConvertir(cot)}
                                                >
                                                    ⚡ Facturar
                                                </button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {historialCotizaciones.length === 0 && (
                                <tr>
                                    <td colSpan="6" style={{ textAlign: 'center' }}>No hay cotizaciones registradas</td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            )}
        </div>
    );
};

export default Cotizaciones;
