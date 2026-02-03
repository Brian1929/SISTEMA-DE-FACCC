import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Productos from './pages/Productos';
import Facturas from './pages/Facturas';
import Historial from './pages/Historial';
import Cotizaciones from './pages/Cotizaciones';
import Configuracion from './pages/Configuracion';
import { getConfig } from './services/api';
import './App.css';

function App() {
  const [config, setConfig] = useState({ nombre_sistema: 'Sistema de Facturación' });

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await getConfig();
      setConfig(response.data);
    } catch (error) {
      console.error('Error al cargar configuración:', error);
    }
  };

  return (
    <Router
      future={{
        v7_relativeSplatPath: true,
        v7_startTransition: true,
      }}
    >
      <div className="app">
        <Navbar nombreSistema={config.nombre_sistema || 'Sistema de Facturación'} />
        <main className="main-content">
          <div className="container">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/productos" element={<Productos />} />
              <Route path="/facturas" element={<Facturas />} />
              <Route path="/historial" element={<Historial />} />
              <Route path="/cotizaciones" element={<Cotizaciones />} />
              <Route path="/configuracion" element={<Configuracion onConfigUpdate={loadConfig} />} />
            </Routes>
          </div>
        </main>
        <footer className="footer">
          <div className="container">
            <p>&copy; 2026 Sistema de Facturación. Todos los derechos reservados.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;

