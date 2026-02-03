# Sistema de Facturación - Versión React

Sistema completo de facturación con frontend en React y backend en Flask.

## 🚀 Estructura del Proyecto

```
.
├── api.py                 # Backend Flask (API REST)
├── frontend/              # Aplicación React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas principales
│   │   ├── services/      # Servicios API
│   │   └── App.jsx        # Componente principal
│   ├── package.json
│   └── vite.config.js
├── producto.py
├── factura.py
├── impresor.py
└── configuracion.py
```

## 📦 Instalación

### Backend (Flask)

1. Instale las dependencias de Python:
```bash
pip install -r requirements.txt
```

### Frontend (React)

1. Navegue a la carpeta frontend:
```bash
cd frontend
```

2. Instale las dependencias de Node.js:
```bash
npm install
```

## 🏃 Ejecución

### 1. Iniciar el Backend (Terminal 1)

```bash
python api.py
```

El servidor Flask estará disponible en: `http://localhost:5000`

### 2. Iniciar el Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

La aplicación React estará disponible en: `http://localhost:3000`

## ✨ Características

- ✅ Frontend moderno con React
- ✅ API REST con Flask
- ✅ Numeración automática de facturas
- ✅ Gestión de productos
- ✅ Creación de facturas con múltiples items
- ✅ Vista previa de facturas
- ✅ Generación de PDF
- ✅ Configuración personalizable
- ✅ Diseño responsive

## 🛠️ Tecnologías Utilizadas

### Frontend
- React 18
- React Router DOM
- Axios
- Vite
- CSS3

### Backend
- Flask
- Flask-CORS
- ReportLab (para PDFs)

## 📝 Scripts Disponibles

### Frontend
- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye la aplicación para producción
- `npm run preview` - Previsualiza la build de producción

## 🔧 Configuración

El sistema se puede configurar desde la página de Configuración en la interfaz web:
- Nombre del sistema
- Prefijo de factura
- Formato de número de factura
- Impuesto por defecto

## 📄 API Endpoints

### Configuración
- `GET /api/configuracion` - Obtener configuración
- `POST /api/configuracion` - Actualizar configuración

### Productos
- `GET /api/productos` - Listar productos
- `POST /api/productos` - Crear producto
- `GET /api/productos/<codigo>` - Obtener producto

### Facturas
- `GET /api/facturas/numero` - Obtener número de factura
- `POST /api/facturas` - Crear factura
- `POST /api/facturas/imprimir` - Generar PDF

### Formatos e Impresores
- `GET /api/formatos` - Listar formatos de papel
- `GET /api/impresores` - Listar tipos de impresores

## 🚀 Despliegue

### Backend
El backend Flask puede desplegarse en cualquier servidor que soporte Python/Flask.

### Frontend
Para construir la aplicación React para producción:

```bash
cd frontend
npm run build
```

Los archivos estáticos estarán en `frontend/dist/` y pueden servirse con cualquier servidor web estático o integrarse con el backend Flask.

## 📝 Notas

- El proxy de Vite está configurado para redirigir las peticiones `/api` al backend en `localhost:5000`
- Asegúrese de que ambos servidores estén corriendo para que la aplicación funcione correctamente
- Los cambios en la configuración se guardan en `config.json`

