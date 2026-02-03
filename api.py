"""
API Flask para el Sistema de Facturación
Backend API puro sin templates HTML.
"""

import os
from flask import Flask, request, jsonify, send_file, send_from_directory
from producto import Producto, CatalogoProductos
from factura import Factura, ItemFactura
from impresor import GestorImpresion
from configuracion import Configuracion
from gestor_facturas import GestorFacturas
from datetime import datetime
import os
from cotizacion import Cotizacion
from gestor_cotizaciones import GestorCotizaciones

app = Flask(__name__, static_folder='frontend/dist')

# CORS manual si flask_cors no está disponible
try:
    from flask_cors import CORS
    CORS(app)
    print("✓ Flask-CORS instalado y configurado")
except ImportError:
    # Implementación manual de CORS
    print("⚠ Flask-CORS no está instalado, usando CORS manual")
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

# Instancias globales
catalogo = CatalogoProductos()
gestor = GestorImpresion()
config = Configuracion()
gestor_facturas = GestorFacturas()  # Gestor para guardar facturas
gestor_cotizaciones = GestorCotizaciones() # Nuevo gestor de cotizaciones

# Inicializar datos de ejemplo si no hay productos
if len(catalogo.listar_productos()) == 0:
    print("📦 No hay productos, se inicializarán al iniciar el servidor")

# Productos de ejemplo (solo si no hay productos guardados)
def inicializar_datos():
    """Inicializa el catálogo con productos de ejemplo solo si está vacío."""
    try:
        if len(catalogo.listar_productos()) == 0:
            print("📦 Inicializando productos de ejemplo...")
            productos_ejemplo = [
                Producto("001", "Laptop Dell", 850.00, "Laptop Dell Inspiron 15", "unidad"),
                Producto("002", "Mouse Logitech", 25.50, "Mouse inalámbrico", "unidad"),
                Producto("003", "Teclado Mecánico", 75.00, "Teclado mecánico RGB", "unidad"),
                Producto("004", "Monitor 24 pulgadas", 200.00, "Monitor Full HD", "unidad"),
                Producto("005", "Cable HDMI", 12.00, "Cable HDMI 2.0", "unidad"),
            ]
            for producto in productos_ejemplo:
                catalogo.agregar_producto(producto)
            print(f"✓ {len(productos_ejemplo)} productos de ejemplo agregados")
        else:
            print(f"✓ Productos cargados desde archivo: {len(catalogo.listar_productos())} productos")
    except Exception as e:
        print(f"⚠ Error en inicializar_datos: {str(e)}")
        import traceback
        traceback.print_exc()


# ============ CONFIGURACIÓN ============

@app.route('/api/configuracion', methods=['GET', 'OPTIONS'])
def api_obtener_configuracion():
    """API para obtener la configuración del sistema."""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        configuraciones = config.obtener_todas_configuraciones()
        
        # Asegurar que todos los valores sean serializables a JSON
        config_serializable = {}
        for key, value in configuraciones.items():
            # Convertir valores no serializables
            if isinstance(value, (int, float, str, bool, type(None))):
                config_serializable[key] = value
            elif isinstance(value, datetime):
                config_serializable[key] = value.isoformat()
            else:
                config_serializable[key] = str(value)
        
        return jsonify(config_serializable), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("=" * 50)
        print("ERROR EN api_obtener_configuracion:")
        print(f"Mensaje: {str(e)}")
        print(f"Traceback completo:")
        print(error_trace)
        print("=" * 50)
        
        # Retornar configuración por defecto en caso de error
        return jsonify({
            'nombre_sistema': 'Sistema de Facturación',
            'ultimo_numero_factura': 0,
            'prefijo_factura': 'FAC',
            'formato_factura': '{prefijo}-{año}-{numero:04d}',
            'impuesto_default': 16.0,
            'error': str(e)
        }), 200


@app.route('/api/configuracion', methods=['POST', 'OPTIONS'])
def api_actualizar_configuracion():
    """API para actualizar la configuración del sistema."""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400
        
        print(f"📥 Actualizando configuración: {data}")
        
        if 'nombre_sistema' in data:
            nombre = str(data['nombre_sistema']).strip()
            if nombre:
                config.establecer_nombre_sistema(nombre)
        
        configuraciones_permitidas = [
            'prefijo_factura', 'formato_factura', 'impuesto_default',
            'nombre_empresa', 'direccion_empresa', 'telefono_empresa', 
            'email_empresa', 'rfc_empresa', 'color_factura', 'firma_autorizado',
            'logo_empresa'
        ]
        actualizaciones = {}
        for clave in configuraciones_permitidas:
            if clave in data:
                valor = data[clave]
                # Validar y convertir según el tipo
                if clave == 'impuesto_default':
                    try:
                        valor = float(valor)
                        if valor < 0:
                            return jsonify({'success': False, 'message': 'El impuesto no puede ser negativo'}), 400
                    except (ValueError, TypeError):
                        return jsonify({'success': False, 'message': 'El impuesto debe ser un número válido'}), 400
                else:
                    valor = str(valor).strip()
                
                actualizaciones[clave] = valor
        
        if actualizaciones:
            config.actualizar_configuraciones(actualizaciones)
            print(f"✓ Configuración actualizada: {actualizaciones}")
        
        # Obtener configuración actualizada y serializarla
        config_actualizada = config.obtener_todas_configuraciones()
        config_serializable = {}
        for key, value in config_actualizada.items():
            if isinstance(value, (int, float, str, bool, type(None))):
                config_serializable[key] = value
            else:
                config_serializable[key] = str(value)
        
        return jsonify({
            'success': True,
            'message': 'Configuración actualizada exitosamente',
            'config': config_serializable
        }), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("=" * 50)
        print("ERROR EN api_actualizar_configuracion:")
        print(f"Mensaje: {str(e)}")
        print(f"Traceback completo:")
        print(error_trace)
        print("=" * 50)
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


# ============ PRODUCTOS ============

@app.route('/api/productos', methods=['GET', 'OPTIONS'])
def api_productos():
    """API para obtener todos los productos."""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        # Obtener productos del catálogo
        productos_lista = catalogo.listar_productos()
        
        # Si no hay productos, inicializar con ejemplos
        if len(productos_lista) == 0:
            try:
                inicializar_datos()
                productos_lista = catalogo.listar_productos()
            except Exception as e:
                print(f"⚠ Error al inicializar datos: {str(e)}")
        
        # Convertir productos a diccionario de forma segura
        productos_json = []
        for p in productos_lista:
            try:
                productos_json.append({
                    'codigo': str(p.codigo) if p.codigo else '',
                    'nombre': str(p.nombre) if p.nombre else '',
                    'precio': float(p.precio) if p.precio is not None else 0.0,
                    'descripcion': str(p.descripcion) if p.descripcion else None,
                    'unidad': str(p.unidad) if p.unidad else 'unidad',
                    'stock': float(p.stock) if p.stock is not None else 0.0
                })
            except Exception as e:
                print(f"⚠ Error al convertir producto {p}: {str(e)}")
                continue
        
        return jsonify(productos_json), 200
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        error_msg = str(e)
        print("=" * 50)
        print("ERROR EN api_productos (GET):")
        print(f"Mensaje: {error_msg}")
        print(f"Traceback completo:")
        print(error_trace)
        print("=" * 50)
        
        # Retornar lista vacía en caso de error para que el frontend no se rompa
        return jsonify([]), 200


@app.route('/api/productos', methods=['POST', 'OPTIONS'])
def api_agregar_producto():
    """API para agregar un producto."""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400
        
        print(f"📥 Datos recibidos: {data}")
        
        # Validar y procesar campos requeridos de forma segura
        codigo = str(data.get('codigo', '')).strip() if data.get('codigo') else ''
        nombre = str(data.get('nombre', '')).strip() if data.get('nombre') else ''
        
        if not codigo:
            return jsonify({'success': False, 'message': 'El código es requerido'}), 400
        if not nombre:
            return jsonify({'success': False, 'message': 'El nombre es requerido'}), 400
        
        # Validar que el código no exista ya
        if catalogo.obtener_producto(codigo):
            return jsonify({'success': False, 'message': f'Ya existe un producto con el código {codigo}'}), 400
        
        # Validar y convertir precio
        precio_str = data.get('precio', '0')
        try:
            if isinstance(precio_str, str):
                precio = float(precio_str) if precio_str else 0.0
            else:
                precio = float(precio_str)
            
            if precio < 0:
                return jsonify({'success': False, 'message': 'El precio no puede ser negativo'}), 400
        except (ValueError, TypeError) as e:
            return jsonify({'success': False, 'message': f'El precio debe ser un número válido. Recibido: {precio_str}'}), 400
        
        # Procesar descripción y unidad de forma segura
        descripcion = None
        if data.get('descripcion'):
            descripcion_str = str(data.get('descripcion', '')).strip()
            descripcion = descripcion_str if descripcion_str else None
        
        unidad = 'unidad'
        if data.get('unidad'):
            unidad_str = str(data.get('unidad', 'unidad')).strip()
            unidad = unidad_str if unidad_str else 'unidad'
        
        stock = float(data.get('stock', 0))
        
        print(f"📦 Creando producto: código={codigo}, nombre={nombre}, precio={precio}")
        
        # Crear producto
        try:
            producto = Producto(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                descripcion=descripcion,
                unidad=unidad,
                stock=stock
            )
            print(f"✓ Producto creado exitosamente")
        except Exception as e:
            print(f"✗ Error al crear objeto Producto: {str(e)}")
            return jsonify({'success': False, 'message': f'Error al crear producto: {str(e)}'}), 400
        
        # Agregar y guardar
        try:
            catalogo.agregar_producto(producto)
            print(f"✓ Producto agregado al catálogo y guardado")
        except Exception as e:
            print(f"✗ Error al agregar producto al catálogo: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'message': f'Error al guardar producto: {str(e)}'}), 500
        
        return jsonify({
            'success': True, 
            'message': 'Producto agregado exitosamente',
            'producto': {
                'codigo': producto.codigo,
                'nombre': producto.nombre,
                'precio': producto.precio
            }
        }), 201
        
    except ValueError as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 400
    except KeyError as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': f'Campo faltante: {str(e)}'}), 400
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print("=" * 50)
        print("ERROR EN api_agregar_producto:")
        print(f"Mensaje: {str(e)}")
        print(f"Traceback completo:")
        print(error_trace)
        print("=" * 50)
        return jsonify({
            'success': False, 
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/api/productos/<codigo>', methods=['GET'])
def api_obtener_producto(codigo):
    """API para obtener un producto por código."""
    producto = catalogo.obtener_producto(codigo)
    if producto:
        return jsonify({
            'codigo': producto.codigo,
            'nombre': producto.nombre,
            'precio': producto.precio,
            'descripcion': producto.descripcion,
            'unidad': producto.unidad,
            'stock': producto.stock
        })
    return jsonify({'error': 'Producto no encontrado'}), 404


@app.route('/api/productos/<codigo>', methods=['PUT', 'OPTIONS'])
def api_actualizar_producto(codigo):
    """API para actualizar un producto existente."""
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.json
        producto_existente = catalogo.obtener_producto(codigo)
        if not producto_existente:
            return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
        
        # Actualizar campos
        nombre = data.get('nombre', producto_existente.nombre)
        precio = float(data.get('precio', producto_existente.precio))
        descripcion = data.get('descripcion', producto_existente.descripcion)
        unidad = data.get('unidad', producto_existente.unidad)
        stock = float(data.get('stock', producto_existente.stock))
        
        producto_actualizado = Producto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            descripcion=descripcion,
            unidad=unidad,
            stock=stock
        )
        
        catalogo.agregar_producto(producto_actualizado)
        return jsonify({'success': True, 'message': 'Producto actualizado correctamente'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400


@app.route('/api/productos/<codigo>', methods=['DELETE', 'OPTIONS'])
def api_eliminar_producto(codigo):
    """API para eliminar un producto."""
    if request.method == 'OPTIONS':
        return '', 200
    
    success = catalogo.eliminar_producto(codigo)
    if success:
        return jsonify({'success': True, 'message': 'Producto eliminado correctamente'})
    return jsonify({'success': False, 'message': 'No se pudo eliminar el producto'}), 400


# ============ FACTURAS ============

@app.route('/api/facturas/numero', methods=['GET'])
def api_obtener_numero_factura():
    """API para obtener un nuevo número de factura."""
    numero = config.generar_numero_factura()
    return jsonify({'numero': numero})


@app.route('/api/facturas', methods=['POST'])
def api_crear_factura():
    """API para crear una factura."""
    try:
        data = request.json
        
        numero_factura = data.get('numero')
        if not numero_factura:
            numero_factura = config.generar_numero_factura()
        
        factura = Factura(
            numero=numero_factura,
            cliente=data['cliente'],
            impuesto=float(data.get('impuesto', config.obtener('impuesto_default', 16.0))),
            notas=data.get('notas')
        )
        
        es_vista_previa = data.get('es_vista_previa', False)
        
        # Validar stock primero
        items_a_crear = []
        for item_data in data['items']:
            producto = catalogo.obtener_producto(item_data['codigo'])
            if not producto:
                return jsonify({'success': False, 'message': f'Producto {item_data["codigo"]} no encontrado'}), 400
            
            cantidad = float(item_data['cantidad'])
            # Validar stock siempre
            if producto.stock < cantidad:
                return jsonify({
                    'success': False, 
                    'message': f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}, Solicitado: {cantidad}'
                }), 400
            
            items_a_crear.append((producto, cantidad))
        
        # Solo descontar y guardar si NO es vista previa
        if not es_vista_previa:
            for producto, cantidad in items_a_crear:
                item = ItemFactura(producto=producto, cantidad=cantidad)
                factura.agregar_item(item)
                
                # Descontar stock
                producto.stock -= cantidad
                catalogo.agregar_producto(producto)
            
            if factura.esta_vacia():
                return jsonify({'success': False, 'message': 'La factura no puede estar vacía'}), 400
            
            # Guardar factura en DB
            gestor_facturas.agregar_factura(factura)
            
            # Si viene de una cotización, actualizar su estado
            origen_cotizacion = data.get('origen_cotizacion')
            if origen_cotizacion:
                try:
                    cot = gestor_cotizaciones.obtener(origen_cotizacion)
                    if cot and cot.estado != 'Facturada':
                        cot.estado = 'Facturada'
                        gestor_cotizaciones.guardar(cot)
                        print(f"✓ Cotización {origen_cotizacion} marcada como Facturada")
                except Exception as e:
                    print(f"⚠ Error al actualizar cotización {origen_cotizacion}: {e}")
        else:
            # Para vista previa, solo llenar el objeto factura sin tocar stock ni DB
            for producto, cantidad in items_a_crear:
                item = ItemFactura(producto=producto, cantidad=cantidad)
                factura.agregar_item(item)
        
        resultado_texto = gestor.imprimir(factura, tipo_impresor="texto", formato_papel="normal")
        
        return jsonify({
            'success': True,
            'factura': {
                'numero': factura.numero,
                'cliente': factura.cliente,
                'fecha': factura.fecha.isoformat(),
                'subtotal': factura.calcular_subtotal(),
                'impuesto': factura.calcular_impuesto(),
                'total': factura.calcular_total(),
                'items': len(factura.items),
                'vista_previa': resultado_texto
            }
        }), 201
        
    except ValueError as e:
        return jsonify({'success': False, 'message': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/facturas/imprimir', methods=['POST'])
def api_imprimir_factura():
    """API para imprimir/generar PDF de una factura."""
    try:
        data = request.json
        if not data:
            return jsonify({'success': False, 'message': 'No se recibieron datos'}), 400
        
        print(f"📥 Solicitud de impresión recibida para factura: {data.get('numero')}")
        
        numero_factura = data.get('numero')
        
        # Intentar cargar factura existente si se proporciona número
        factura = None
        factura_guardada = None
        if numero_factura:
            factura_guardada = gestor_facturas.obtener_factura(numero_factura)
            if factura_guardada:
                factura = factura_guardada
                print(f"📄 Usando factura guardada encontrada: {numero_factura}")
        
        # Si no existe o no se proporcionó número, crear una nueva
        if not factura:
            if not numero_factura:
                numero_factura = config.generar_numero_factura()
            
            try:
                cliente = data.get('cliente', 'Cliente General')
                items_list = data.get('items', [])
            except Exception as e:
                return jsonify({'success': False, 'message': f'Error en datos: {str(e)}'}), 400
            
            factura = Factura(
                numero=numero_factura,
                cliente=cliente,
                impuesto=float(data.get('impuesto', config.obtener('impuesto_default', 16.0))),
                notas=data.get('notas')
            )
            
            for item_data in items_list:
                codigo = item_data.get('codigo')
                if not codigo:
                    continue
                    
                producto = catalogo.obtener_producto(codigo)
                if not producto:
                    print(f"⚠ Producto {codigo} no encontrado al crear factura")
                    continue
                
        # Si no existe cargar los items y validar stock
        if not factura_guardada:
            items_a_crear = []
            for item_data in items_list:
                codigo = item_data.get('codigo')
                if not codigo: continue
                
                producto = catalogo.obtener_producto(codigo)
                if not producto: continue
                
                cantidad = float(item_data.get('cantidad', 1))
                if producto.stock < cantidad:
                    return jsonify({'success': False, 'message': f'Stock insuficiente para {producto.nombre}'}), 400
                
                items_a_crear.append((producto, cantidad))
            
            for producto, cantidad in items_a_crear:
                item = ItemFactura(producto=producto, cantidad=cantidad)
                factura.agregar_item(item)
                # Descontar stock al imprimir/guardar nueva factura
                producto.stock -= cantidad
                catalogo.agregar_producto(producto)
            
            if factura.esta_vacia():
                return jsonify({'success': False, 'message': 'La factura no tiene productos'}), 400
            
            # Guardar factura en DB
            try:
                gestor_facturas.agregar_factura(factura)
            except Exception as e:
                print(f"⚠ Error al guardar: {str(e)}")
            
             # Si viene de una cotización, actualizar su estado (igual que en crear_factura)
            origen_cotizacion = data.get('origen_cotizacion')
            if origen_cotizacion:
                try:
                    cot = gestor_cotizaciones.obtener(origen_cotizacion)
                    if cot and cot.estado != 'Facturada':
                        cot.estado = 'Facturada'
                        gestor_cotizaciones.guardar(cot)
                        print(f"✓ Cotización {origen_cotizacion} marcada como Facturada desde Impresión/PDF")
                except Exception as e:
                    print(f"⚠ Error al actualizar cotización {origen_cotizacion}: {e}")
        else:
            # Si ya existía, usamos los items que ya tenía el objeto factura (cargado de DB)
            pass
        
        tipo_impresor = data.get('tipo_impresor', 'pdf')
        formato_papel = data.get('formato_papel', 'normal')
        
        if tipo_impresor == 'pdf':
            try:
                resultado = gestor.imprimir(factura, tipo_impresor=tipo_impresor, formato_papel=formato_papel)
                
                # Si el resultado es bytes (PDF generado), retornarlo directamente
                if isinstance(resultado, (bytes, bytearray)):
                    from flask import Response
                    nombre_archivo = f"factura_{factura.numero}.pdf"
                    
                    response = Response(
                        resultado,
                        mimetype='application/pdf',
                        headers={
                            'Content-Disposition': f'attachment; filename={nombre_archivo}'
                        }
                    )
                    return response
                else:
                    return jsonify({
                        'success': False, 
                        'message': 'El generador de PDF no retornó datos válidos'
                    }), 500
                        
            except Exception as e:
                import traceback
                error_trace = traceback.format_exc()
                with open("error_pdf.log", "w") as f:
                    f.write(error_trace)
                print(f"✗ Error al generar PDF: {str(e)}")
                return jsonify({
                    'success': False, 
                    'message': f'Error al generar PDF: {str(e)}'
                }), 500
        else:
            resultado = gestor.imprimir(factura, tipo_impresor=tipo_impresor, formato_papel=formato_papel)
            return jsonify({'success': True, 'vista_previa': str(resultado)}), 200
            
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        with open("error_reportlab.log", "w") as f:
            f.write(error_trace)
        print(f"✗ Error crítico en api_imprimir_factura: {str(e)}")
        return jsonify({'success': False, 'message': f'Error interno: {str(e)}'}), 500


@app.route('/api/facturas', methods=['GET'])
def api_listar_facturas():
    """API para listar todas las facturas guardadas."""
    try:
        facturas = gestor_facturas.listar_facturas()
        facturas_json = []
        
        for f in facturas:
            facturas_json.append({
                'numero': f.numero,
                'cliente': f.cliente,
                'fecha': f.fecha.isoformat(),
                'subtotal': f.calcular_subtotal(),
                'impuesto': f.calcular_impuesto(),
                'total': f.calcular_total(),
                'items_count': len(f.items)
            })
        
        return jsonify({
            'success': True,
            'facturas': facturas_json,
            'total': len(facturas_json)
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/facturas/<numero>', methods=['GET'])
def api_obtener_factura_guardada(numero):
    """API para obtener una factura guardada por número."""
    try:
        factura = gestor_facturas.obtener_factura(numero)
        
        if not factura:
            return jsonify({'success': False, 'message': 'Factura no encontrada'}), 404
        
        items_json = []
        for item in factura.items:
            items_json.append({
                'producto': {
                    'codigo': item.producto.codigo,
                    'nombre': item.producto.nombre,
                    'precio': item.producto.precio
                },
                'cantidad': item.cantidad,
                'subtotal': item.calcular_subtotal()
            })
        
        return jsonify({
            'success': True,
            'factura': {
                'numero': factura.numero,
                'cliente': factura.cliente,
                'fecha': factura.fecha.isoformat(),
                'impuesto': factura.impuesto,
                'notas': factura.notas,
                'items': items_json,
                'subtotal': factura.calcular_subtotal(),
                'impuesto_monto': factura.calcular_impuesto(),
                'total': factura.calcular_total()
            }
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


@app.route('/api/facturas/estadisticas', methods=['GET'])
def api_estadisticas_facturas():
    """API para obtener estadísticas de facturas y alertas de stock."""
    try:
        stats = gestor_facturas.obtener_estadisticas()
        
        # Obtener alertas de stock bajo (<= 5)
        productos = catalogo.listar_productos()
        bajo_stock = []
        for p in productos:
            if p.stock <= 5:
                bajo_stock.append({
                    'codigo': p.codigo,
                    'nombre': p.nombre,
                    'stock': p.stock,
                    'unidad': p.unidad
                })
        
        stats['productos_bajo_stock'] = bajo_stock
        stats['conteo_bajo_stock'] = len(bajo_stock)
        
        return jsonify({
            'success': True,
            'estadisticas': stats
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'}), 500


# ============ FORMATOS E IMPRESORES ============

@app.route('/api/formatos', methods=['GET'])
def api_formatos():
    """API para obtener los formatos de papel disponibles."""
    formatos = gestor.listar_formatos()
    return jsonify(formatos)


@app.route('/api/impresores', methods=['GET'])
def api_impresores():
    """API para obtener los tipos de impresores disponibles."""
    impresores = gestor.listar_impresores()
    return jsonify(impresores)


# ============ COTIZACIONES ============

@app.route('/api/cotizaciones/numero', methods=['GET'])
def api_obtener_numero_cotizacion():
    try:
        # Usar la misma lógica correlativa pero con prefijo COT
        conteo = gestor_cotizaciones.coleccion.count_documents({}) + 1
        anio = datetime.now().year
        numero = f"COT-{anio}-{conteo:04d}"
        return jsonify({'numero': numero}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cotizaciones', methods=['GET', 'POST'])
def api_cotizaciones():
    if request.method == 'GET':
        try:
            cotizaciones = gestor_cotizaciones.listar()
            resultado = []
            for cot in cotizaciones:
                resultado.append({
                    'numero': cot.numero,
                    'cliente': cot.cliente,
                    'fecha': cot.fecha.isoformat(),
                    'total': cot.calcular_total(),
                    'estado': cot.estado
                })
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
            
    elif request.method == 'POST':
        try:
            data = request.json
            items_list = data.get('items', [])
            
            cot = Cotizacion(
                numero=data['numero'],
                cliente=data['cliente'],
                impuesto=float(data.get('impuesto', config.obtener('impuesto_default', 16.0))),
                notas=data.get('notas'),
                estado="Pendiente"
            )
            
            for item_data in items_list:
                producto = catalogo.obtener_producto(item_data['codigo'])
                if producto:
                    item = ItemFactura(producto, float(item_data['cantidad']))
                    cot.agregar_item(item)
            
            gestor_cotizaciones.guardar(cot)
            return jsonify({'success': True, 'message': 'Cotización guardada'}), 201
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cotizaciones/imprimir', methods=['POST'])
def api_imprimir_cotizacion():
    try:
        data = request.json
        numero = data.get('numero')
        cot = gestor_cotizaciones.obtener(numero)
        
        # Si no existe en DB, intentamos crearla temporal para el PDF (desde los datos del form)
        if not cot:
            cot = Cotizacion(
                numero=numero,
                cliente=data.get('cliente', 'Cliente General'),
                impuesto=float(data.get('impuesto', 16.0)),
                notas=data.get('notas')
            )
            for item_data in data.get('items', []):
                p = catalogo.obtener_producto(item_data['codigo'])
                if p:
                    cot.agregar_item(ItemFactura(p, float(item_data['cantidad'])))
        
        resultado = gestor.imprimir(cot, tipo_impresor='pdf')
        
        from flask import Response
        response = Response(
            resultado,
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=cotizacion_{numero}.pdf'
            }
        )
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cotizaciones/<numero>', methods=['GET'])
def api_obtener_cotizacion(numero):
    try:
        # Decodificar por si viene con caracteres especiales, aunque el numero suele ser limpio
        import urllib.parse
        numero = urllib.parse.unquote(numero)
        cot = gestor_cotizaciones.obtener(numero)
        if cot:
            return jsonify({'success': True, 'cotizacion': cot.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Cotización no encontrada'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/cotizaciones/convertir', methods=['POST'])
def api_convertir_cotizacion():
    try:
        data = request.json
        numero_cot = data.get('numero')
        cot = gestor_cotizaciones.obtener(numero_cot)
        
        if not cot:
            return jsonify({'success': False, 'message': 'Cotización no encontrada'}), 404
            
        if cot.estado == 'Facturada':
            return jsonify({'success': False, 'message': 'Esta cotización ya fue facturada'}), 400
            
        # 1. Crear Factura a partir de Cotización
        conteo = gestor_facturas.coleccion.count_documents({}) + 1
        anio = datetime.now().year
        numero_fact = f"FACT-{anio}-{conteo:04d}"
        
        factura_nueva = Factura(
            numero=numero_fact,
            cliente=cot.cliente,
            fecha=datetime.now(),
            impuesto=cot.impuesto,
            notas=f"Basado en cotización {cot.numero}. {cot.notas or ''}"
        )
        
        # 2. Validar Stock y Agregar Items
        for item_cot in cot.items:
            producto = catalogo.obtener_producto(item_cot.producto.codigo)
            if not producto:
                 return jsonify({'success': False, 'message': f'Producto {item_cot.producto.codigo} ya no existe'}), 400
            
            # Verificar si es tipo 'unidad' para validar stock
            if producto.unidad == 'unidad' and producto.stock < item_cot.cantidad:
                return jsonify({'success': False, 'message': f'Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}'}), 400
                
            # Agregar a factura
            item_fact = ItemFactura(producto, item_cot.cantidad)
            factura_nueva.agregar_item(item_fact)
            
        # 3. Guardar Factura (esto descuenta stock automáticamente en la lógica de negocio si existiera, pero aquí lo hacemos manual o confiamos en el gestor)
        # Nota: En este diseño, la clase GestorFacturas solo guarda en Mongo. El descuento de stock se hacía en el endpoint de '/api/facturas'.
        # Debemos replicar la lógica de descuento de stock aquí.
        
        for item in factura_nueva.items:
            if item.producto.unidad == 'unidad':
                catalogo.actualizar_stock(item.producto.codigo, -item.cantidad)
        
        gestor_facturas.agregar_factura(factura_nueva)
        
        # 4. Actualizar estado de Cotización
        cot.estado = 'Facturada'
        gestor_cotizaciones.guardar(cot)
        
        return jsonify({
            'success': True, 
            'message': f'Cotización convertida en Factura {numero_fact}',
            'nueva_factura': numero_fact
        }), 201
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

# ============ RUTAS FRONTEND ============
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    # Si se pide un archivo específico (ej. assets/index.css) y existe, servirlo
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Si no, siempre servir index.html (SPA)
    else:
        return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    # Asegurar que los datos estén inicializados antes de iniciar
    try:
        inicializar_datos()
        print("✓ Datos inicializados correctamente")
        print(f"✓ Productos cargados: {len(catalogo.listar_productos())}")
    except Exception as e:
        print(f"⚠ Error al inicializar datos: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print("🚀 Iniciando servidor Flask en http://localhost:5000")
    print("📡 API disponible en http://localhost:5000/api")
    app.run(debug=True, host='0.0.0.0', port=5000)
    # Reload server trigger

