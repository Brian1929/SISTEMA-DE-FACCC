
import urllib.request
import urllib.parse
import urllib.error
import json

BASE_URL = "http://localhost:5000/api"

def test_get_cotizacion():
    print("🚀 Probando GET Cotización...")
    
    # 1. Listar para obtener un ID válido
    try:
        req = urllib.request.Request(f"{BASE_URL}/cotizaciones")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if not data:
                print("❌ No hay cotizaciones para probar")
                return
            
            cot_num = data[0]['numero']
            print(f"ℹ Probando con cotización: {cot_num}")
            
            # 2. Get individual
            encoded_num = urllib.parse.quote(cot_num)
            
            req_single = urllib.request.Request(f"{BASE_URL}/cotizaciones/{encoded_num}")
            with urllib.request.urlopen(req_single) as res_single:
                if res_single.getcode() == 200:
                    cot_data = json.loads(res_single.read().decode('utf-8'))
                    print("✓ Cotización obtenida exitosamente:")
                    # Verificar estructura
                    if 'cotizacion' in cot_data:
                         c = cot_data['cotizacion']
                         print(f"   Cliente: {c.get('cliente')}")
                         print(f"   Items: {len(c.get('items', []))}")
                         print(f"   Total: {c.get('total')}")
                    else:
                        print("❌ Respuesta inesperada:", cot_data)
                else:
                     print(f"❌ Error HTTP: {res_single.getcode()}")

    except urllib.error.HTTPError as e:
        print(f"❌ Error HTTP: {e.code} - {e.read().decode('utf-8')}")
    except Exception as e:
        print(f"❌ Excepción: {e}")

if __name__ == "__main__":
    test_get_cotizacion()
