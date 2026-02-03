"""
Módulo para manejo de facturas en el sistema de facturación.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from producto import Producto


@dataclass
class ItemFactura:
    """Representa un item en una factura."""
    
    producto: Producto
    cantidad: float
    
    def __post_init__(self):
        """Valida que la cantidad sea positiva."""
        if self.cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero")
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal del item."""
        return self.producto.calcular_subtotal(self.cantidad)


@dataclass
class Factura:
    """Clase que representa una factura."""
    
    numero: str
    cliente: str
    fecha: datetime = field(default_factory=datetime.now)
    items: list[ItemFactura] = field(default_factory=list)
    impuesto: float = 0.0  # Porcentaje de impuesto
    notas: Optional[str] = None
    
    def agregar_item(self, item: ItemFactura) -> None:
        """Agrega un item a la factura."""
        self.items.append(item)
    
    def calcular_subtotal(self) -> float:
        """Calcula el subtotal de la factura."""
        return sum(item.calcular_subtotal() for item in self.items)
    
    def calcular_impuesto(self) -> float:
        """Calcula el monto del impuesto."""
        return self.calcular_subtotal() * (self.impuesto / 100)
    
    def calcular_total(self) -> float:
        """Calcula el total de la factura."""
        return self.calcular_subtotal() + self.calcular_impuesto()
    
    def obtener_cantidad_items(self) -> int:
        """Retorna la cantidad de items en la factura."""
        return len(self.items)
    
    def esta_vacia(self) -> bool:
        """Verifica si la factura está vacía."""
        return len(self.items) == 0

