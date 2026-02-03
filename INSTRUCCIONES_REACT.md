# Instrucciones - Sistema de Facturación con React

## 🚀 Inicio Rápido

### Paso 1: Instalar Dependencias del Backend

```bash
python -m pip install -r requirements.txt
```

O si tiene pip directamente:
```bash
pip install -r requirements.txt
```

### Paso 2: Instalar Dependencias del Frontend

```bash
cd frontend
npm install
```

### Paso 3: Iniciar el Sistema

**Opción A: Usar los scripts de Windows**

1. Abra una terminal y ejecute:
   ```bash
   iniciar_backend.bat
   ```

2. Abra otra terminal y ejecute:
   ```bash
   iniciar_frontend.bat
   ```

**Opción B: Manual**

1. Terminal 1 - Backend:
   ```bash
   python api.py
   ```
   El backend estará en: http://localhost:5000

2. Terminal 2 - Frontend:
   ```bash
   cd frontend
   npm run dev
   ```
   El frontend estará en: http://localhost:3000

## 📋 Uso del Sistema

1. Abra su navegador en: **http://localhost:3000**

2. El sistema tiene las siguientes secciones:
   - **Inicio**: Dashboard con estadísticas
   - **Productos**: Gestión de productos
   - **Facturas**: Crear facturas
   - **Configuración**: Personalizar el sistema

## ✨ Características

- ✅ Interfaz moderna con React
- ✅ API REST con Flask
- ✅ Numeración automática de facturas
- ✅ Vista previa de facturas
- ✅ Generación de PDF
- ✅ Configuración personalizable

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask_cors'"
**Solución**: Instale flask-cors:
```bash
python -m pip install flask-cors
```

### Error: "npm no se reconoce como comando"
**Solución**: Instale Node.js desde https://nodejs.org/

### El frontend no se conecta al backend
**Solución**: 
- Asegúrese de que el backend esté corriendo en puerto 5000
- Verifique que el proxy en `frontend/vite.config.js` apunte a `http://localhost:5000`

### Puerto 3000 o 5000 ya está en uso
**Solución**: 
- Cambie el puerto en `frontend/vite.config.js` (frontend)
- Cambie el puerto en `api.py` línea final (backend)

## 📝 Notas Importantes

- **Ambos servidores deben estar corriendo** para que la aplicación funcione
- El backend maneja toda la lógica de negocio
- El frontend solo se comunica con el backend mediante API REST
- Los cambios en configuración se guardan en `config.json`

