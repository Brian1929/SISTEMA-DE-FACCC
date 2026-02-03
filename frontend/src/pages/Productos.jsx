import { useState, useEffect } from 'react';
import { getProductos, createProducto, updateProducto, deleteProducto } from '../services/api';
import Modal from '../components/Modal';
import './Productos.css';

function Productos() {
  const [productos, setProductos] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    codigo: '',
    nombre: '',
    precio: '',
    descripcion: '',
    unidad: 'unidad',
    stock: '0.0'
  });
  const [isEditing, setIsEditing] = useState(false);
  const [editingCodigo, setEditingCodigo] = useState(null);

  useEffect(() => {
    loadProductos();
  }, []);

  const loadProductos = async () => {
    try {
      const response = await getProductos();
      setProductos(response.data);
    } catch (error) {
      console.error('Error al cargar productos:', error);
      const errorMessage = error.response?.data?.message || error.message || 'Error desconocido';
      alert('Error al cargar productos: ' + errorMessage);
      // Intentar mostrar productos vacíos en caso de error
      setProductos([]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar que los campos requeridos estén llenos
    if (!formData.codigo || !formData.nombre || !formData.precio) {
      alert('✗ Por favor complete todos los campos requeridos (Código, Nombre, Precio)');
      return;
    }

    try {
      // Asegurar que el precio sea un número
      const datosEnviar = {
        ...formData,
        precio: parseFloat(formData.precio) || 0,
        stock: parseFloat(formData.stock) || 0
      };

      console.log('Enviando datos:', datosEnviar);

      const response = isEditing
        ? await updateProducto(editingCodigo, datosEnviar)
        : await createProducto(datosEnviar);

      if (response.data && response.data.success) {
        alert(isEditing ? '✓ Producto actualizado' : '✓ Producto agregado');
        handleCloseModal();
        // Recargar productos después de un breve delay para asegurar que se guardó
        setTimeout(() => {
          loadProductos();
        }, 300);
      } else {
        const errorMsg = response.data?.message || 'Error desconocido';
        alert('✗ Error: ' + errorMsg);
        console.error('Respuesta del servidor:', response.data);
      }
    } catch (error) {
      console.error('Error completo:', error);
      console.error('Error response:', error.response);

      let errorMessage = 'Error al agregar producto';

      if (error.response) {
        // El servidor respondió con un código de error
        errorMessage = error.response.data?.message ||
          error.response.data?.error ||
          `Error ${error.response.status}: ${error.response.statusText}`;
      } else if (error.request) {
        // La petición se hizo pero no hubo respuesta
        errorMessage = 'No se pudo conectar con el servidor. Verifique que el backend esté corriendo.';
      } else {
        errorMessage = error.message || 'Error desconocido';
      }

      alert('✗ Error: ' + errorMessage);
    }
  };

  const handleEdit = (producto) => {
    setIsEditing(true);
    setEditingCodigo(producto.codigo);
    setFormData({
      codigo: producto.codigo,
      nombre: producto.nombre,
      precio: producto.precio.toString(),
      descripcion: producto.descripcion || '',
      unidad: producto.unidad || 'unidad',
      stock: producto.stock.toString()
    });
    setShowModal(true);
  };

  const handleDelete = async (codigo) => {
    if (window.confirm(`¿Está seguro de eliminar el producto ${codigo}?`)) {
      try {
        const response = await deleteProducto(codigo);
        if (response.data.success) {
          alert('✓ Producto eliminado');
          loadProductos();
        }
      } catch (error) {
        alert('✗ Error al eliminar: ' + error.message);
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setIsEditing(false);
    setEditingCodigo(null);
    setFormData({ codigo: '', nombre: '', precio: '', descripcion: '', unidad: 'unidad', stock: '0.0' });
  };

  return (
    <div className="productos-page">
      <div className="page-header">
        <h1>Gestión de Productos</h1>
        <button className="btn btn-primary" onClick={() => { setIsEditing(false); setShowModal(true); }}>
          ➕ Agregar Producto
        </button>
      </div>

      <div className="table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Descripción</th>
              <th>Precio</th>
              <th>Stock</th>
              <th>Unidad</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            {productos.length === 0 ? (
              <tr>
                <td colSpan="7" style={{ textAlign: 'center', padding: '2rem', color: '#64748b' }}>
                  No hay productos registrados. Agregue uno para comenzar.
                </td>
              </tr>
            ) : (
              productos.map((producto) => (
                <tr key={producto.codigo}>
                  <td><strong>{producto.codigo}</strong></td>
                  <td>{producto.nombre}</td>
                  <td>{producto.descripcion || '-'}</td>
                  <td>${parseFloat(producto.precio).toFixed(2)}</td>
                  <td style={{ fontWeight: 'bold', color: parseFloat(producto.stock) <= 5 ? '#e74c3c' : 'inherit' }}>
                    {parseFloat(producto.stock).toFixed(2)}
                  </td>
                  <td>{producto.unidad}</td>
                  <td>
                    <div className="action-btns">
                      <button className="btn-icon edit" title="Editar" onClick={() => handleEdit(producto)}>✏️</button>
                      <button className="btn-icon delete" title="Eliminar" onClick={() => handleDelete(producto.codigo)}>🗑️</button>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <Modal show={showModal} onClose={handleCloseModal} title={isEditing ? "Editar Producto" : "Agregar Producto"}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Código *</label>
            <input
              type="text"
              value={formData.codigo}
              onChange={(e) => setFormData({ ...formData, codigo: e.target.value })}
              required
              disabled={isEditing}
            />
          </div>
          <div className="form-group">
            <label>Nombre *</label>
            <input
              type="text"
              value={formData.nombre}
              onChange={(e) => setFormData({ ...formData, nombre: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Precio *</label>
            <input
              type="number"
              step="0.01"
              min="0"
              value={formData.precio}
              onChange={(e) => setFormData({ ...formData, precio: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Descripción</label>
            <textarea
              rows="3"
              value={formData.descripcion}
              onChange={(e) => setFormData({ ...formData, descripcion: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>Stock Inicial *</label>
            <input
              type="number"
              step="0.01"
              value={formData.stock}
              onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
              required
            />
          </div>
          <div className="form-group">
            <label>Unidad</label>
            <input
              type="text"
              value={formData.unidad}
              onChange={(e) => setFormData({ ...formData, unidad: e.target.value })}
            />
          </div>
          <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
            <button type="button" className="btn btn-secondary" onClick={handleCloseModal}>
              Cancelar
            </button>
            <button type="submit" className="btn btn-primary">Guardar</button>
          </div>
        </form>
      </Modal>
    </div>
  );
}

export default Productos;

