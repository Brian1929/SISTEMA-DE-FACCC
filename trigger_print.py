
import urllib.request
import json

def trigger():
    url = "http://localhost:5000/api/facturas/imprimir"
    data = {
        "numero": "FINAL-TEST",
        "cliente": "Test User",
        "impuesto": 16.0,
        "notas": "Nota de prueba final",
        "items": [
            {"codigo": "TEST", "cantidad": 1}
        ],
        "tipo_impresor": "pdf",
        "formato_papel": "normal"
    }
    
    try:
        print(f"Enviando petición a {url}...")
        req = urllib.request.Request(
            url, 
            data=json.dumps(data).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req) as response:
                print(f"Status Code: {response.getcode()}")
                content = response.read()
                print(f"Recibidos {len(content)} bytes.")
                with open("trigger_result.pdf", "wb") as f:
                    f.write(content)
                print("✓ PDF guardado en trigger_result.pdf")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error: {e.code}")
            print("Response:", e.read().decode('utf-8'))
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    trigger()
