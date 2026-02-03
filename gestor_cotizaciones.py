
from datetime import datetime
from typing import List, Optional, Dict, Any
from cotizacion import Cotizacion
from factura import ItemFactura
from producto import Producto
from db import db

class GestorCotizaciones:
    """Gestor para guardar y cargar cotizaciones desde MongoDB Atlas."""
    
    def __init__(self):
        self.coleccion = db.cotizaciones
    
    def _cotizacion_a_dict(self, cot: Cotizacion) -> Dict[str, Any]:
        return {
            "numero": cot.numero,
            "cliente": cot.cliente,
            "fecha": cot.fecha,
            "impuesto": cot.impuesto,
            "notas": cot.notas,
            "estado": cot.estado,
            "items": [
                {
                    "producto": {
                        "codigo": item.producto.codigo,
                        "nombre": item.producto.nombre,
                        "precio": item.producto.precio
                    },
                    "cantidad": item.cantidad
                }
                for item in cot.items
            ]
        }
    
    def _dict_a_cotizacion(self, data: Dict[str, Any]) -> Cotizacion:
        cot = Cotizacion(
            numero=data["numero"],
            cliente=data["cliente"],
            fecha=data.get("fecha") if isinstance(data.get("fecha"), datetime) else datetime.now(),
            impuesto=data.get("impuesto", 0.0),
            notas=data.get("notas"),
            estado=data.get("estado", "Pendiente")
        )
        
        for item_data in data.get("items", []):
            p_data = item_data["producto"]
            producto = Producto(p_data["codigo"], p_data["nombre"], p_data["precio"])
            item = ItemFactura(producto, item_data["cantidad"])
            cot.agregar_item(item)
            
        return cot
    
    def guardar(self, cot: Cotizacion) -> None:
        if self.obtener(cot.numero):
            self.coleccion.replace_one({"numero": cot.numero}, self._cotizacion_a_dict(cot))
        else:
            self.coleccion.insert_one(self._cotizacion_a_dict(cot))
            
    def obtener(self, numero: str) -> Optional[Cotizacion]:
        doc = self.coleccion.find_one({"numero": numero})
        return self._dict_a_cotizacion(doc) if doc else None
    
    def listar(self) -> List[Cotizacion]:
        docs = self.coleccion.find().sort("fecha", -1)
        return [self._dict_a_cotizacion(doc) for doc in docs]

    def eliminar(self, numero: str) -> bool:
        result = self.coleccion.delete_one({"numero": numero})
        return result.deleted_count > 0
