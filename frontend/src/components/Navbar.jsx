import { Link, useLocation } from 'react-router-dom';
import './Navbar.css';

function Navbar({ nombreSistema }) {
  const location = useLocation();

  return (
    <nav className="navbar">
      <div className="container">
        <div className="nav-brand">
          <h1>📄 {nombreSistema}</h1>
        </div>
        <ul className="nav-menu">
          <li>
            <Link
              to="/"
              className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}
            >
              Inicio
            </Link>
          </li>
          <li>
            <Link
              to="/productos"
              className={`nav-link ${location.pathname === '/productos' ? 'active' : ''}`}
            >
              Productos
            </Link>
          </li>
          <li>
            <Link
              to="/facturas"
              className={`nav-link ${location.pathname === '/facturas' ? 'active' : ''}`}
            >
              Facturas
            </Link>
          </li>
          <li>
            <Link
              to="/historial"
              className={`nav-link ${location.pathname === '/historial' ? 'active' : ''}`}
            >
              Historial
            </Link>
          </li>
          <li>
            <Link
              to="/cotizaciones"
              className={`nav-link ${location.pathname === '/cotizaciones' ? 'active' : ''}`}
            >
              Cotizaciones
            </Link>
          </li>
          <li>
            <Link
              to="/configuracion"
              className={`nav-link ${location.pathname === '/configuracion' ? 'active' : ''}`}
            >
              ⚙️ Configuración
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  );
}

export default Navbar;

