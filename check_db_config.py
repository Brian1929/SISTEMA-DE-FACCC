
from db import db
import base64

def check_config():
    try:
        config_doc = db.configuracion.find_one()
        if not config_doc:
            print("✗ No se encontró documento de configuración.")
            return
            
        print("✓ Configuración encontrada.")
        logo = config_doc.get("logo_empresa", "")
        if logo:
            print(f"✓ Logo detectado. Longitud: {len(logo)} caracteres.")
            if "," in logo:
                header, data = logo.split(",", 1)
                print(f"  - Header: {header}")
                try:
                    decoded = base64.b64decode(data)
                    print(f"  - Decodificación exitosa. Tamaño: {len(decoded)} bytes.")
                except Exception as e:
                    print(f"  - ✗ Error de decodificación: {str(e)}")
            else:
                print("  - ⚠ Logo no tiene header data:image/...")
        else:
            print("  - Sin logo configurado.")
            
    except Exception as e:
        print(f"✗ Error al conectar a DB: {str(e)}")

if __name__ == "__main__":
    check_config()
