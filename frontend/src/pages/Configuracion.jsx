import { useState, useEffect } from 'react';
import { getConfig, updateConfig } from '../services/api';
import './Configuracion.css';

function Configuracion({ onConfigUpdate }) {
  const [config, setConfig] = useState({
    nombre_sistema: 'Sistema de Facturación',
    prefijo_factura: 'FAC',
    formato_factura: '{prefijo}-{año}-{numero:04d}',
    impuesto_default: 16.0,
    nombre_empresa: '',
    direccion_empresa: '',
    telefono_empresa: '',
    email_empresa: '',
    rfc_empresa: '',
    color_factura: '#27AE60',
    firma_autorizado: '',
    logo_empresa: '',
    ultimo_numero_factura: 0
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await getConfig();
      setConfig(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error al cargar configuración:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await updateConfig({
        nombre_sistema: config.nombre_sistema,
        prefijo_factura: config.prefijo_factura,
        formato_factura: config.formato_factura,
        impuesto_default: config.impuesto_default,
        nombre_empresa: config.nombre_empresa,
        direccion_empresa: config.direccion_empresa,
        telefono_empresa: config.telefono_empresa,
        email_empresa: config.email_empresa,
        rfc_empresa: config.rfc_empresa,
        color_factura: config.color_factura,
        firma_autorizado: config.firma_autorizado || '',
        logo_empresa: config.logo_empresa || ''
      });
      alert('✓ Configuración guardada exitosamente');
      if (onConfigUpdate) {
        onConfigUpdate();
      }
    } catch (error) {
      alert('✗ Error: ' + (error.response?.data?.message || error.message));
    }
  };

  const restaurarDefault = () => {
    if (window.confirm('¿Está seguro de restaurar los valores por defecto?')) {
      setConfig({
        ...config,
        nombre_sistema: 'Sistema de Facturación',
        prefijo_factura: 'FAC',
        formato_factura: '{prefijo}-{año}-{numero:04d}',
        impuesto_default: 16.0,
        nombre_empresa: 'Mi Empresa S.A. de C.V.',
        direccion_empresa: 'Av. Principal #123, Col. Centro, Ciudad, CP 12345',
        telefono_empresa: 'Tel: (555) 123-4567',
        email_empresa: 'Brianpolanco95@gmail.com',
        rfc_empresa: '',
        color_factura: '#27AE60',
        firma_autorizado: 'Gerente General',
        logo_empresa: ''
      });
    }
  };

  const generarVistaPrevia = () => {
    const año = new Date().getFullYear();
    const numero = (config.ultimo_numero_factura || 0) + 1;
    return config.formato_factura
      .replace('{prefijo}', config.prefijo_factura || 'FAC')
      .replace('{año}', año)
      .replace('{numero:04d}', String(numero).padStart(4, '0'))
      .replace('{numero}', numero);
  };

  const handleLogoChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 500000) { // 500kb limit
        alert('La imagen es muy pesada. Favor use una menor a 500kb.');
        return;
      }
      const reader = new FileReader();
      reader.onloadend = () => {
        setConfig({ ...config, logo_empresa: reader.result });
      };
      reader.readAsDataURL(file);
    }
  };

  if (loading) {
    return <div>Cargando configuración...</div>;
  }

  return (
    <div className="configuracion-page">
      <div className="page-header">
        <h1>⚙️ Configuración del Sistema</h1>
      </div>

      <div className="card">
        <h3>Configuración General</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Nombre del Sistema *</label>
            <input
              type="text"
              value={config.nombre_sistema}
              onChange={(e) => setConfig({ ...config, nombre_sistema: e.target.value })}
              required
              placeholder="Ej: Mi Empresa - Sistema de Facturación"
            />
            <small>Este nombre aparecerá en la barra de navegación y en las facturas</small>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Prefijo de Factura</label>
              <input
                type="text"
                value={config.prefijo_factura}
                onChange={(e) => setConfig({ ...config, prefijo_factura: e.target.value })}
                placeholder="Ej: FAC, INV, BOL"
              />
              <small>Prefijo para los números de factura (ej: FAC-2024-0001)</small>
            </div>
            <div className="form-group">
              <label>Impuesto por Defecto (%)</label>
              <input
                type="number"
                value={config.impuesto_default}
                onChange={(e) => setConfig({ ...config, impuesto_default: parseFloat(e.target.value) || 0 })}
                step="0.01"
                min="0"
              />
              <small>Porcentaje de impuesto que se usará por defecto en nuevas facturas</small>
            </div>
          </div>

          <div className="form-divider" style={{ margin: '2rem 0', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
            <h3>🏢 Datos de la Empresa (Facturas)</h3>
            <p style={{ color: '#64748b', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
              Esta información aparecerá en el encabezado de todas tus facturas generadas.
            </p>
          </div>

          <div className="form-group">
            <label>Nombre Fiscal / Empresa *</label>
            <input
              type="text"
              value={config.nombre_empresa}
              onChange={(e) => setConfig({ ...config, nombre_empresa: e.target.value })}
              required
              placeholder="Ej: BrianTech"
            />
          </div>

          <div className="form-group">
            <label>Dirección Completa</label>
            <input
              type="text"
              value={config.direccion_empresa}
              onChange={(e) => setConfig({ ...config, direccion_empresa: e.target.value })}
              placeholder="Ej: Santiago, Republica Dominicana"
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Teléfono de Contacto</label>
              <input
                type="text"
                value={config.telefono_empresa}
                onChange={(e) => setConfig({ ...config, telefono_empresa: e.target.value })}
                placeholder="Ej: (849)-711-2919"
              />
            </div>
            <div className="form-group">
              <label>Email de Contacto</label>
              <input
                type="email"
                value={config.email_empresa}
                onChange={(e) => setConfig({ ...config, email_empresa: e.target.value })}
                placeholder="Ej: brianpolanco95@gmail.com"
              />
            </div>
          </div>

          <div className="form-group">
            <label>RFC / ID Fiscal</label>
            <input
              type="text"
              value={config.rfc_empresa}
              onChange={(e) => setConfig({ ...config, rfc_empresa: e.target.value })}
              placeholder="Ej: RFC: BRP950101XXX"
            />
          </div>

          <div className="form-group">
            <label>Nombre para Firma Digital (Autorizado por)</label>
            <input
              type="text"
              value={config.firma_autorizado}
              onChange={(e) => setConfig({ ...config, firma_autorizado: e.target.value })}
              placeholder="Ej: Ing. Brian Polanco o Gerencia General"
            />
            <small>Este nombre aparecerá en letra cursiva elegante sobre la línea de firma en el PDF.</small>
          </div>

          <div className="form-group">
            <label>Logo de la Empresa</label>
            <div className="logo-upload-container">
              <div className="logo-preview-area">
                {config.logo_empresa ? (
                  <img src={config.logo_empresa} alt="Logo Empresa" className="logo-preview-img" />
                ) : (
                  <div className="logo-placeholder">Sin Logo</div>
                )}
              </div>
              <div className="logo-upload-actions">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleLogoChange}
                  id="logo-input"
                  style={{ display: 'none' }}
                />
                <button
                  type="button"
                  className="btn btn-secondary"
                  onClick={() => document.getElementById('logo-input').click()}
                >
                  {config.logo_empresa ? 'Cambiar Logo' : 'Subir Logo'}
                </button>
                {config.logo_empresa && (
                  <button
                    type="button"
                    className="btn btn-danger-outline"
                    onClick={() => setConfig({ ...config, logo_empresa: '' })}
                  >
                    Eliminar
                  </button>
                )}
              </div>
            </div>
            <small>Se recomienda una imagen cuadrada o rectangular (PNG o JPG) de máximo 500kb.</small>
          </div>

          <div className="form-group">
            <label>Color Principal de la Factura</label>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <input
                type="color"
                value={config.color_factura}
                onChange={(e) => setConfig({ ...config, color_factura: e.target.value })}
                style={{ width: '60px', height: '40px', padding: '2px', cursor: 'pointer' }}
              />
              <span>{config.color_factura.toUpperCase()}</span>
            </div>
            <small>Este color se aplicará a los encabezados y elementos principales del PDF</small>
          </div>

          <div className="form-divider" style={{ margin: '2rem 0', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
            <h3>🔢 Numeración de Facturas</h3>
          </div>

          <div className="form-group">
            <label>Formato de Número de Factura</label>
            <input
              type="text"
              value={config.formato_factura}
              onChange={(e) => setConfig({ ...config, formato_factura: e.target.value })}
              placeholder="{prefijo}-{año}-{numero:04d}"
            />
            <small>
              Formato: {'{prefijo}'} = prefijo, {'{año}'} = año actual, {'{numero:04d}'} = número con 4 dígitos
              <br />Ejemplo: {'{prefijo}'}-{'{año}'}-{'{numero:04d}'} genera: FAC-2024-0001
            </small>
          </div>

          <div className="info-box">
            <strong>ℹ️ Información:</strong>
            <ul>
              <li>El número de factura se genera automáticamente y es único</li>
              <li>Los cambios en el formato afectarán solo a las nuevas facturas</li>
              <li>El contador actual de facturas: <strong>{config.ultimo_numero_factura || 0}</strong></li>
            </ul>
          </div>

          <div className="form-group">
            <label>Vista Previa del Formato</label>
            <div className="preview-box">
              <strong>Próximo número de factura:</strong>
              <span className="preview-numero">{generarVistaPrevia()}</span>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end', marginTop: '2rem' }}>
            <button type="button" className="btn btn-secondary" onClick={restaurarDefault}>
              🔄 Restaurar Valores por Defecto
            </button>
            <button type="submit" className="btn btn-primary">
              💾 Guardar Configuración
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Configuracion;

