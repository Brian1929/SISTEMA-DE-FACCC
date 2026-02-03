
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from producto import Producto
from factura import ItemFactura

@dataclass
class Cotizacion:
    """Clase que representa una cotización o presupuesto."""
    
    numero: str
    cliente: str
    fecha: datetime = field(default_factory=datetime.now)
    items: list[ItemFactura] = field(default_factory=list)
    impuesto: float = 0.0
    notas: Optional[str] = None
    estado: str = "Pendiente" # Pendiente, Aceptada, Facturada, Rechazada
    
    def agregar_item(self, item: ItemFactura) -> None:
        self.items.append(item)
    
    def calcular_subtotal(self) -> float:
        return sum(item.calcular_subtotal() for item in self.items)
    
    def calcular_impuesto(self) -> float:
        return self.calcular_subtotal() * (self.impuesto / 100)
    
    def calcular_total(self) -> float:
        return self.calcular_subtotal()
    
    def to_dict(self) -> dict:
        return {
            "numero": self.numero,
            "cliente": self.cliente,
            "fecha": self.fecha.isoformat(),
            "items": [
                {
                    "producto": {
                        "codigo": item.producto.codigo,
                        "nombre": item.producto.nombre,
                        "precio": item.producto.precio,
                        "stock": item.producto.stock
                    },
                    "cantidad": item.cantidad,
                    "precio": item.producto.precio,
                    "subtotal": item.calcular_subtotal()
                } for item in self.items
            ],
            "impuesto": 0,
            "subtotal": self.calcular_subtotal(),
            "total": self.calcular_total(),
            "notas": self.notas,
            "estado": self.estado
        }
    
    def esta_vacia(self) -> bool:
        return len(self.items) == 0
