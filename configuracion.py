"""
Módulo para gestión de configuración del sistema en MongoDB Atlas.
"""

from typing import Dict, Any
from datetime import datetime
from db import db


class Configuracion:
    """Clase para manejar la configuración del sistema en MongoDB."""
    
    def __init__(self):
        """Inicializa la conexión con la colección de configuración."""
        self.coleccion = db.configuracion
        self._config = self._cargar_config()
    
    def _cargar_config(self) -> Dict[str, Any]:
        """Carga la configuración desde MongoDB Atlas."""
        # Configuración por defecto
        config_default = {
            "nombre_sistema": "Sistema de Facturación",
            "ultimo_numero_factura": 0,
            "prefijo_factura": "FAC",
            "formato_factura": "{prefijo}-{año}-{numero:04d}",
            "impuesto_default": 16.0,
            "nombre_empresa": "BrianTech",
            "direccion_empresa": "Santiago, Republica Dominicana",
            "telefono_empresa": "(849)-711-2919",
            "email_empresa": "Brianpolanco95@gmail.com",
            "rfc_empresa": "",
            "color_factura": "#27AE60",
            "firma_autorizado": "Gerente General",
            "logo_empresa": "", # Logo en Base64
        }
        
        try:
            doc = self.coleccion.find_one()
            if not doc:
                # Si no hay config en Mongo, insertar la default
                self.coleccion.insert_one(config_default.copy())
                return config_default
            
            # Asegurar que todas las claves por defecto estén presentes (schema migration)
            for key, value in config_default.items():
                if key not in doc:
                    doc[key] = value
            return doc
        except Exception as e:
            print(f"⚠ Error al cargar configuración de Mongo: {str(e)}")
            return config_default

    def _guardar_config(self) -> None:
        """Sincroniza la configuración actual con MongoDB Atlas."""
        try:
            # Limpiar el campo _id si existe antes de actualizar (o usar update_one)
            self.coleccion.update_one({}, {"$set": self._config}, upsert=True)
        except Exception as e:
            print(f"✗ Error al guardar configuración en Atlas: {str(e)}")

    def obtener(self, clave: str, valor_default: Any = None) -> Any:
        """Obtiene un valor de configuración."""
        return self._config.get(clave, valor_default)
    
    def establecer(self, clave: str, valor: Any) -> None:
        """Establece un valor de configuración."""
        self._config[clave] = valor
        self._guardar_config()
    
    def obtener_nombre_sistema(self) -> str:
        """Obtiene el nombre del sistema."""
        return self.obtener("nombre_sistema", "Sistema de Facturación")
    
    def establecer_nombre_sistema(self, nombre: str) -> None:
        """Establece el nombre del sistema."""
        self.establecer("nombre_sistema", nombre)
    
    def generar_numero_factura(self) -> str:
        """Genera un número de factura único automáticamente."""
        ultimo_numero = self.obtener("ultimo_numero_factura", 0)
        nuevo_numero = ultimo_numero + 1
        self.establecer("ultimo_numero_factura", nuevo_numero)
        
        formato = self.obtener("formato_factura", "{prefijo}-{año}-{numero:04d}")
        prefijo = self.obtener("prefijo_factura", "FAC")
        año = datetime.now().year
        
        numero_factura = formato.format(
            prefijo=prefijo,
            año=año,
            numero=nuevo_numero
        )
        return numero_factura
    
    def obtener_todas_configuraciones(self) -> Dict[str, Any]:
        """Obtiene todas las configuraciones serializables."""
        config_copy = self._config.copy()
        if "_id" in config_copy:
            del config_copy["_id"] # No enviar el ID interno de Mongo al frontend
        return config_copy
    
    def actualizar_configuraciones(self, configuraciones: Dict[str, Any]) -> None:
        """Actualiza múltiples configuraciones a la vez."""
        for clave, valor in configuraciones.items():
            self._config[clave] = valor
        self._guardar_config()

