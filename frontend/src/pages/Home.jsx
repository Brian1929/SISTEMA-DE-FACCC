import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getEstadisticas } from '../services/api';
import './Home.css';

function Home() {
  const [stats, setStats] = useState({
    total_facturas: 0,
    total_ventas: 0,
    promedio_venta: 0,
    productos_bajo_stock: [],
    conteo_bajo_stock: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setLoading(true);
      const response = await getEstadisticas();
      if (response.data.success) {
        setStats(response.data.estadisticas);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
      setLoading(false);
    }
  };

  return (
    <div className="home-dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Panel de Control</h1>
          <p>Bienvenido al sistema de gestión de facturación corporativa.</p>
        </div>
        <div className="current-date">
          {new Date().toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </div>
      </header>

      <section className="stats-grid">
        <div className="stat-card-premium sales">
          <div className="stat-icon">💰</div>
          <div className="stat-info">
            <span className="stat-label">Ventas Totales</span>
            <h2 className="stat-value">
              {loading ? '...' : `$${parseFloat(stats.total_ventas).toLocaleString('es-ES', { minimumFractionDigits: 2 })}`}
            </h2>
          </div>
        </div>

        <div className="stat-card-premium invoices">
          <div className="stat-icon">📄</div>
          <div className="stat-info">
            <span className="stat-label">Facturas Emitidas</span>
            <h2 className="stat-value">{loading ? '...' : stats.total_facturas}</h2>
          </div>
        </div>

        <div className="stat-card-premium average">
          <div className="stat-icon">📈</div>
          <div className="stat-info">
            <span className="stat-label">Promedio de Venta</span>
            <h2 className="stat-value">
              {loading ? '...' : `$${parseFloat(stats.promedio_venta).toLocaleString('es-ES', { minimumFractionDigits: 2 })}`}
            </h2>
          </div>
        </div>

        <div className="stat-card-premium inventory" style={{ borderLeftColor: stats.conteo_bajo_stock > 0 ? '#e74c3c' : '#27ae60' }}>
          <div className="stat-icon">{stats.conteo_bajo_stock > 0 ? '⚠️' : '✅'}</div>
          <div className="stat-info">
            <span className="stat-label">Alertas de Stock</span>
            <h2 className="stat-value" style={{ color: stats.conteo_bajo_stock > 0 ? '#e74c3c' : 'inherit' }}>
              {loading ? '...' : stats.conteo_bajo_stock}
            </h2>
          </div>
        </div>
      </section>

      {stats.productos_bajo_stock && stats.productos_bajo_stock.length > 0 && (
        <section className="inventory-alerts">
          <h3 className="section-title">⚠️ Productos con Stock Bajo</h3>
          <div className="alerts-list">
            {stats.productos_bajo_stock.map(p => (
              <div key={p.codigo} className="alert-item">
                <span className="alert-code">{p.codigo}</span>
                <span className="alert-name">{p.nombre}</span>
                <span className="alert-stock">Quedan: <strong>{p.stock}</strong> {p.unidad}</span>
                <Link to="/productos" className="btn-refill">Reabastecer</Link>
              </div>
            ))}
          </div>
        </section>
      )}

      <h3 className="section-title">Acciones Rápidas</h3>
      <section className="actions-grid">
        <Link to="/facturas" className="action-card">
          <div className="action-icon plus">+</div>
          <div className="action-details">
            <h4>Nueva Factura</h4>
            <p>Generar un nuevo comprobante para un cliente.</p>
          </div>
        </Link>

        <Link to="/historial" className="action-card">
          <div className="action-icon history">📋</div>
          <div className="action-details">
            <h4>Historial</h4>
            <p>Ver y reimprimir facturas anteriores.</p>
          </div>
        </Link>

        <Link to="/productos" className="action-card">
          <div className="action-icon box">📦</div>
          <div className="action-details">
            <h4>Productos</h4>
            <p>Gestionar catálogo y precios de inventario.</p>
          </div>
        </Link>
        <Link to="/configuracion" className="action-card">
          <div className="action-icon gear">⚙️</div>
          <div className="action-details">
            <h4>Configuración</h4>
            <p>Ajustes del sistema y datos fiscales.</p>
          </div>
        </Link>
      </section>

      <footer className="dashboard-footer">
        <p>Sistema de Facturación Profesional © 2026</p>
      </footer>
    </div>
  );
}

export default Home;

