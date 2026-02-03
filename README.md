# Sistema de Facturación Web

Sistema completo de facturación desarrollado en Python con interfaz web moderna usando Flask. Soporte para productos, precios y múltiples formatos de impresión.

## Características

- ✅ **Interfaz Web Moderna**: Aplicación web responsive con diseño profesional
- ✅ Gestión completa de productos con código, nombre, precio y descripción
- ✅ Creación de facturas con múltiples items desde la interfaz web
- ✅ Cálculo automático de subtotales, impuestos y totales en tiempo real
- ✅ Soporte para descuentos por item
- ✅ Sistema extensible de impresión con múltiples formatos de papel
- ✅ Impresión en formato texto (vista previa) y PDF (descarga)
- ✅ API REST para integración con otros sistemas
- ✅ Arquitectura modular y fácil de extender

## Formatos de Papel Soportados

1. **Papel Normal (A4)** - Formato estándar de oficina
2. **Papel Térmico (80mm)** - Para impresoras térmicas
3. **Papel Carta (8.5x11)** - Formato carta estadounidense

## Instalación

1. Asegúrese de tener Python 3.7 o superior instalado.

2. Instale las dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Iniciar la aplicación web

1. Instale las dependencias:
```bash
pip install -r requirements.txt
```

2. Inicie el servidor web:
```bash
python app.py
```

3. Abra su navegador y visite:
```
http://localhost:5000
```

### Funcionalidades de la interfaz web

- **Inicio**: Dashboard con estadísticas y acceso rápido a las funciones
- **Productos**: Gestión completa de productos (agregar, editar, listar)
- **Facturas**: Crear facturas con interfaz intuitiva:
  - Agregar múltiples productos
  - Aplicar descuentos por item
  - Vista previa antes de imprimir
  - Generar PDF para descarga

## Estructura del Proyecto

```
.
├── app.py               # Aplicación Flask (servidor web)
├── producto.py          # Clases para manejo de productos
├── factura.py           # Clases para manejo de facturas
├── impresor.py          # Sistema de impresión extensible
├── main.py              # Aplicación de consola (opcional)
├── ejemplo.py           # Ejemplo de uso programático
├── requirements.txt     # Dependencias del proyecto
├── templates/           # Plantillas HTML
│   ├── base.html
│   ├── index.html
│   ├── productos.html
│   └── facturas.html
├── static/              # Archivos estáticos
│   └── style.css        # Estilos CSS
└── README.md           # Este archivo
```

## Extender el Sistema

### Agregar un Nuevo Formato de Papel

Para agregar un nuevo formato de papel, cree una clase que herede de `FormatoPapel`:

```python
from impresor import FormatoPapel

class MiNuevoFormato(FormatoPapel):
    @property
    def nombre(self) -> str:
        return "Mi Formato Personalizado"
    
    @property
    def ancho(self) -> float:
        return 150.0  # mm
    
    @property
    def alto(self) -> float:
        return 200.0  # mm
    
    def obtener_configuracion(self) -> Dict[str, Any]:
        return {
            "margen_superior": 15,
            "margen_inferior": 15,
            "margen_izquierdo": 15,
            "margen_derecho": 15,
            "tamano_titulo": 14,
            "tamano_texto": 9,
            "espaciado_linea": 11,
        }
```

Luego regístrelo en el gestor:
```python
gestor.registrar_formato("mi_formato", MiNuevoFormato())
```

### Agregar un Nuevo Tipo de Impresor

Para agregar un nuevo tipo de impresor (por ejemplo, HTML), cree una clase que herede de `ImpresorFactura`:

```python
from impresor import ImpresorFactura, FormatoPapel
from factura import Factura

class ImpresorHTML(ImpresorFactura):
    def imprimir(self, factura: Factura, formato: FormatoPapel) -> str:
        # Implemente la lógica de impresión HTML aquí
        html = f"<html><body><h1>Factura {factura.numero}</h1>...</body></html>"
        # Guardar archivo HTML
        return "Factura generada como HTML"
```

Luego regístrelo:
```python
gestor.registrar_impresor("html", ImpresorHTML())
```

## API REST

El sistema expone una API REST para integración:

### Productos
- `GET /api/productos` - Listar todos los productos
- `POST /api/productos` - Crear un producto
- `GET /api/productos/<codigo>` - Obtener un producto

### Facturas
- `POST /api/facturas` - Crear una factura (retorna vista previa)
- `POST /api/facturas/imprimir` - Generar PDF de factura

### Formatos e Impresores
- `GET /api/formatos` - Listar formatos de papel disponibles
- `GET /api/impresores` - Listar tipos de impresores disponibles

## Ejemplo de Uso Programático

```python
from producto import Producto, CatalogoProductos
from factura import Factura, ItemFactura
from impresor import GestorImpresion

# Crear catálogo y productos
catalogo = CatalogoProductos()
producto = Producto("001", "Producto Ejemplo", 100.00)
catalogo.agregar_producto(producto)

# Crear factura
factura = Factura("FAC-001", "Cliente Ejemplo", impuesto=16.0)
item = ItemFactura(producto, cantidad=2, descuento=10.0)
factura.agregar_item(item)

# Imprimir
gestor = GestorImpresion()
resultado = gestor.imprimir(factura, tipo_impresor="pdf", formato_papel="normal")
print(resultado)
```

## Licencia

Este proyecto es de código abierto y está disponible para uso libre.

