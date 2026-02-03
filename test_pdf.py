
from factura import Factura, ItemFactura
from producto import Producto
from impresor import GestorImpresion
from configuracion import Configuracion
import datetime

def test_pdf():
    try:
        config = Configuracion()
        gestor = GestorImpresion()
        
        # Crear factura de prueba
        p = Producto("TEST", "Producto de Prueba", 100.0)
        item = ItemFactura(p, 1)
        f = Factura("TEST-001", "Cliente de Prueba", datetime.datetime.now())
        f.agregar_item(item)
        f.notas = "Esta es una nota de prueba para verificar HRFlowable"
        
        print("Intentando generar PDF...")
        resultado = gestor.imprimir(f, tipo_impresor="pdf", formato_papel="normal")
        
        if isinstance(resultado, (bytes, bytearray)):
            with open("test_output.pdf", "wb") as out:
                out.write(resultado)
            print("✓ PDF generado exitosamente en test_output.pdf")
        else:
            print(f"✗ Resultado inesperado: {type(resultado)}")
            
    except Exception as e:
        import traceback
        print("✗ ERROR DETECTADO:")
        traceback.print_exc()

if __name__ == "__main__":
    test_pdf()
