"""
Módulo para gestión de persistencia de facturas en MongoDB Atlas.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
from factura import Factura, ItemFactura
from producto import Producto
from db import db


class GestorFacturas:
    """Gestor para guardar y cargar facturas desde MongoDB Atlas."""
    
    def __init__(self):
        """Inicializa el gestor y la conexión a la colección."""
        self.coleccion = db.facturas
    
    def _factura_a_dict(self, factura: Factura) -> Dict[str, Any]:
        """Convierte una factura a diccionario para MongoDB."""
        return {
            "numero": factura.numero,
            "cliente": factura.cliente,
            "fecha": factura.fecha,  # Mongo maneja objetos datetime directamente
            "impuesto": factura.impuesto,
            "notas": factura.notas,
            "items": [
                {
                    "producto": {
                        "codigo": item.producto.codigo,
                        "nombre": item.producto.nombre,
                        "precio": item.producto.precio
                    },
                    "cantidad": item.cantidad
                }
                for item in factura.items
            ]
        }
    
    def _dict_a_factura(self, data: Dict[str, Any]) -> Factura:
        """Convierte un documento de MongoDB a objeto Factura."""
        factura = Factura(
            numero=data["numero"],
            cliente=data["cliente"],
            fecha=data["fecha"] if isinstance(data["fecha"], datetime) else datetime.fromisoformat(data["fecha"]),
            impuesto=data.get("impuesto", 0.0),
            notas=data.get("notas")
        )
        
        for item_data in data.get("items", []):
            producto_data = item_data["producto"]
            producto = Producto(
                codigo=producto_data["codigo"],
                nombre=producto_data["nombre"],
                precio=producto_data["precio"]
            )
            
            item = ItemFactura(
                producto=producto,
                cantidad=item_data["cantidad"]
            )
            
            factura.agregar_item(item)
        
        return factura
    
    def agregar_factura(self, factura: Factura) -> None:
        """Guarda una nueva factura en MongoDB."""
        if self.obtener_factura(factura.numero):
            print(f"⚠ Factura {factura.numero} ya existe en Atlas")
            return
        
        doc = self._factura_a_dict(factura)
        self.coleccion.insert_one(doc)
        print(f"✓ Factura {factura.numero} guardada en Atlas")
    
    def obtener_factura(self, numero: str) -> Optional[Factura]:
        """Obtiene una factura por su número desde MongoDB."""
        doc = self.coleccion.find_one({"numero": numero})
        return self._dict_a_factura(doc) if doc else None
    
    def listar_facturas(self) -> List[Factura]:
        """Retorna todas las facturas de MongoDB."""
        docs = self.coleccion.find().sort("fecha", -1)
        return [self._dict_a_factura(doc) for doc in docs]
    
    def eliminar_factura(self, numero: str) -> bool:
        """Elimina una factura de MongoDB."""
        result = self.coleccion.delete_one({"numero": numero})
        return result.deleted_count > 0
    
    def obtener_cantidad(self) -> int:
        """Retorna la cantidad total de facturas."""
        return self.coleccion.count_documents({})
    
    def buscar_por_cliente(self, cliente: str) -> List[Factura]:
        """Busca facturas por cliente usando regex."""
        docs = self.coleccion.find({
            "cliente": {"$regex": cliente, "$options": "i"}
        })
        return [self._dict_a_factura(doc) for doc in docs]
    
    def obtener_facturas_por_fecha(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Factura]:
        """Busca facturas en un rango de fechas."""
        docs = self.coleccion.find({
            "fecha": {"$gte": fecha_inicio, "$lte": fecha_fin}
        })
        return [self._dict_a_factura(doc) for doc in docs]
    
    def calcular_total_ventas(self) -> float:
        """Calcula el total usando agregación de Mongo."""
        pipeline = [
            {"$project": {
                "total": {
                    "$add": [
                        {"$reduce": {
                            "input": "$items",
                            "initialValue": 0,
                            "in": {"$add": ["$$value", {"$multiply": ["$$this.producto.precio", "$$this.cantidad"]}]}
                        }},
                        {"$multiply": [
                             {"$reduce": {
                                "input": "$items",
                                "initialValue": 0,
                                "in": {"$add": ["$$value", {"$multiply": ["$$this.producto.precio", "$$this.cantidad"]}]}
                            }},
                            {"$divide": ["$impuesto", 100]}
                        ]}
                    ]
                }
            }},
            {"$group": {"_id": None, "total_ventas": {"$sum": "$total"}}}
        ]
        result = list(self.coleccion.aggregate(pipeline))
        return result[0]["total_ventas"] if result else 0.0

    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Genera estadísticas rápidas."""
        facturas = self.listar_facturas()
        if not facturas:
            return {
                "total_facturas": 0,
                "total_ventas": 0.0,
                "promedio_venta": 0.0,
                "factura_mayor": 0,
                "factura_menor": 0
            }
        
        totales = [f.calcular_total() for f in facturas]
        return {
            "total_facturas": len(totales),
            "total_ventas": sum(totales),
            "promedio_venta": sum(totales) / len(totales),
            "factura_mayor": max(totales),
            "factura_menor": min(totales)
        }
