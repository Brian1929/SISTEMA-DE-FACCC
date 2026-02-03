"""
Módulo para manejo de productos en MongoDB Atlas.
"""

from dataclasses import dataclass
from typing import Optional, List
from db import db


@dataclass
class Producto:
    """Clase que representa un producto en el sistema."""
    
    codigo: str
    nombre: str
    precio: float
    descripcion: Optional[str] = None
    unidad: str = "unidad"
    stock: float = 0.0
    
    def __post_init__(self):
        """Valida que el precio sea positivo."""
        if self.precio < 0:
            raise ValueError("El precio no puede ser negativo")
    
    def calcular_subtotal(self, cantidad: float) -> float:
        """Calcula el subtotal para una cantidad dada."""
        return self.precio * cantidad
    
    def __str__(self) -> str:
        return f"{self.nombre} - ${self.precio:.2f} (Stock: {self.stock})"


class CatalogoProductos:
    """Catálogo de productos almacenado en MongoDB Atlas."""
    
    def __init__(self):
        """Inicializa la conexión con la colección de productos."""
        self.coleccion = db.productos
    
    def _doc_a_producto(self, doc: dict) -> Producto:
        """Convierte un documento de Mongo a objeto Producto."""
        return Producto(
            codigo=doc.get('codigo', ''),
            nombre=doc.get('nombre', ''),
            precio=float(doc.get('precio', 0.0)),
            descripcion=doc.get('descripcion'),
            unidad=doc.get('unidad', 'unidad'),
            stock=float(doc.get('stock', 0.0))
        )

    def _producto_a_dict(self, p: Producto) -> dict:
        """Convierte un objeto Producto a diccionario para Mongo."""
        return {
            'codigo': p.codigo,
            'nombre': p.nombre,
            'precio': p.precio,
            'descripcion': p.descripcion,
            'unidad': p.unidad,
            'stock': p.stock
        }

    def agregar_producto(self, producto: Producto) -> None:
        """Agrega o actualiza un producto en MongoDB."""
        self.coleccion.update_one(
            {"codigo": producto.codigo},
            {"$set": self._producto_a_dict(producto)},
            upsert=True
        )
        print(f"✓ Producto {producto.codigo} guardado en Atlas")
    
    def obtener_producto(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por su código desde MongoDB."""
        doc = self.coleccion.find_one({"codigo": codigo})
        return self._doc_a_producto(doc) if doc else None
    
    def listar_productos(self) -> List[Producto]:
        """Lista todos los productos desde MongoDB."""
        docs = self.coleccion.find().sort("nombre", 1)
        return [self._doc_a_producto(doc) for doc in docs]
    
    def buscar_producto(self, termino: str) -> List[Producto]:
        """Busca productos por nombre o código en MongoDB."""
        docs = self.coleccion.find({
            "$or": [
                {"nombre": {"$regex": termino, "$options": "i"}},
                {"codigo": {"$regex": termino, "$options": "i"}}
            ]
        })
        return [self._doc_a_producto(doc) for doc in docs]
    
    def eliminar_producto(self, codigo: str) -> bool:
        """Elimina un producto de MongoDB."""
        result = self.coleccion.delete_one({"codigo": codigo})
        return result.deleted_count > 0

    def actualizar_stock(self, codigo: str, cantidad: float) -> bool:
        """Actualiza el stock de un producto (suma o resta)."""
        result = self.coleccion.update_one(
            {"codigo": codigo},
            {"$inc": {"stock": cantidad}}
        )
        return result.modified_count > 0

