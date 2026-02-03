
import urllib.request
import json
import time

BASE_URL = "http://localhost:5000/api"

def make_request(endpoint, method='GET', data=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {'Content-Type': 'application/json'}
    
    try:
        if data:
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(url, data=json_data, headers=headers, method=method)
        else:
            req = urllib.request.Request(url, headers=headers, method=method)
            
        with urllib.request.urlopen(req) as response:
            return {
                'status': response.getcode(),
                'data': json.loads(response.read().decode('utf-8'))
            }
    except urllib.error.HTTPError as e:
        return {
            'status': e.code,
            'error': e.read().decode('utf-8')
        }
    except Exception as e:
        print(f"Error request: {e}")
        return None

def test_flow():
    print("🚀 Iniciando prueba de flujo de Cotizaciones (urllib)...")
    
    # 1. Obtener número de cotización
    res = make_request("/cotizaciones/numero")
    if not res or res['status'] != 200:
        print(f"❌ Error obteniendo número: {res}")
        return
        
    numero_cot = res['data']['numero']
    print(f"✓ Número obtenido: {numero_cot}")

    # 2. Buscar productos
    res_prod = make_request("/productos")
    if not res_prod or not res_prod['data']:
        print("❌ No hay productos para cotizar")
        return
    
    producto_test = res_prod['data'][0]
    print(f"ℹ Usando producto: {producto_test['nombre']} ({producto_test['codigo']})")

    # 3. Crear Cotización
    cotizacion_data = {
        "numero": numero_cot,
        "cliente": "Cliente Test Flow",
        "notas": "Cotización de prueba para conversión",
        "items": [
            {"codigo": producto_test['codigo'], "cantidad": 1}
        ],
        "impuesto": 16.0
    }
    
    res_create = make_request("/cotizaciones", method='POST', data=cotizacion_data)
    if res_create and res_create['status'] == 201:
        print("✓ Cotización creada exitosamente")
    else:
        print(f"❌ Error al crear cotización: {res_create}")
        return

    # 4. Listar y verificar
    res_list = make_request("/cotizaciones")
    cot_encontrada = next((c for c in res_list['data'] if c['numero'] == numero_cot), None)
    
    if cot_encontrada:
        print(f"✓ Cotización {numero_cot} encontrada en listado con estado: {cot_encontrada['estado']}")
    else:
        print("❌ Cotización no encontrada en listado")
        return

    # 5. Convertir a Factura
    print("⚡ Intentando convertir a factura...")
    res_convert = make_request("/cotizaciones/convertir", method='POST', data={"numero": numero_cot})
    
    if res_convert and res_convert['status'] == 201:
        data_conv = res_convert['data']
        print(f"✓ Conversión exitosa! Nueva factura: {data_conv['nueva_factura']}")
    else:
        print(f"❌ Error al convertir: {res_convert}")
        return

    # 6. Verificar Factura creada
    res_facturas = make_request("/facturas")
    factura_nueva = next((f for f in res_facturas['data'] if f['numero'] == data_conv['nueva_factura']), None)
    
    if factura_nueva:
        print(f"✓ Factura {factura_nueva['numero']} verificada en sistema")
    else:
        print("❌ La factura creada no aparece en el listado")

    # Verificar estado actualizado
    res_list_final = make_request("/cotizaciones")
    cot_final = next((c for c in res_list_final['data'] if c['numero'] == numero_cot), None)
    
    if cot_final and cot_final['estado'] == 'Facturada':
        print("✓ Estado de cotización actualizado correctamente a 'Facturada'")
    else:
        print(f"❌ Estado incorrecto: {cot_final['estado'] if cot_final else 'None'}")

if __name__ == "__main__":
    test_flow()
