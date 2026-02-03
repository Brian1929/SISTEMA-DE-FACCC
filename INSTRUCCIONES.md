# Instrucciones Rápidas - Sistema de Facturación Web

## 🚀 Inicio Rápido

### Opción 1: Usar el script de inicio (Windows)
Simplemente haga doble clic en `iniciar.bat` o ejecute:
```bash
iniciar.bat
```

### Opción 2: Inicio manual
1. Instale las dependencias:
```bash
pip install -r requirements.txt
```

2. Inicie el servidor:
```bash
python app.py
```

3. Abra su navegador en: **http://localhost:5000**

## 📋 Uso del Sistema

### Gestión de Productos
1. Haga clic en **"Productos"** en el menú superior
2. Haga clic en **"➕ Agregar Producto"**
3. Complete el formulario:
   - Código (único)
   - Nombre
   - Precio
   - Descripción (opcional)
   - Unidad (por defecto: "unidad")
4. Haga clic en **"Guardar"**

### Crear una Factura
1. Haga clic en **"Facturas"** en el menú superior
2. Complete la información básica:
   - Número de factura
   - Nombre del cliente
   - Porcentaje de impuesto (por defecto: 16%)
   - Notas (opcional)
3. Agregue productos:
   - Seleccione un producto del menú desplegable
   - Ingrese la cantidad
   - Ingrese el descuento (%) si aplica
   - Haga clic en **"Agregar"**
4. Repita el paso 3 para agregar más productos
5. Revise los totales calculados automáticamente
6. Opciones disponibles:
   - **Vista Previa**: Ver cómo se verá la factura impresa
   - **Generar PDF**: Descargar la factura en formato PDF
   - **Limpiar**: Borrar todos los datos y empezar de nuevo

## 🎨 Características

- ✅ Interfaz web moderna y responsive
- ✅ Cálculo automático de totales en tiempo real
- ✅ Vista previa antes de imprimir
- ✅ Generación de PDF profesional
- ✅ Gestión completa de productos
- ✅ Soporte para múltiples formatos de papel (extensible)

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solución**: Instale Flask ejecutando:
```bash
pip install Flask
```

### Error: "ModuleNotFoundError: No module named 'reportlab'"
**Solución**: Instale reportlab ejecutando:
```bash
pip install reportlab
```

### El servidor no inicia
**Solución**: Verifique que el puerto 5000 no esté en uso. Puede cambiar el puerto editando `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambie 5000 por otro puerto
```

## 📱 Acceso desde otros dispositivos

Si desea acceder desde otros dispositivos en la misma red:
1. Encuentre su dirección IP local (ej: 192.168.1.100)
2. Acceda desde otro dispositivo usando: `http://192.168.1.100:5000`

## 🛑 Detener el Servidor

Presione `Ctrl + C` en la terminal donde está corriendo el servidor.

