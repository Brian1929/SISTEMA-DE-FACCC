"""
Script para migrar datos de productos.json y facturas.json a MongoDB Atlas.
"""

import json
import os
from datetime import datetime
from db import db

def migrar_productos():
    print("📦 Migrando productos...")
    if not os.path.exists("productos.json"):
        print("⚠ No se encontró productos.json")
        return

    try:
        with open("productos.json", 'r', encoding='utf-8') as f:
            productos = json.load(f)
            
        if productos:
            coleccion = db.productos
            # Limpiar colección antes de migrar (opcional, para evitar duplicados en pruebas)
            coleccion.delete_many({})
            coleccion.insert_many(productos)
            print(f"✓ {len(productos)} productos migrados con éxito.")
    except Exception as e:
        print(f"✗ Error al migrar productos: {str(e)}")

def migrar_facturas():
    print("🧾 Migrando facturas...")
    if not os.path.exists("facturas.json"):
        print("⚠ No se encontró facturas.json")
        return

    try:
        with open("facturas.json", 'r', encoding='utf-8') as f:
            facturas = json.load(f)
            
        if facturas:
            coleccion = db.facturas
            coleccion.delete_many({})
            
            # Convertir fechas de string ISO a objetos datetime de Python (requerido por Mongo)
            for f in facturas:
                if 'fecha' in f:
                    f['fecha'] = datetime.fromisoformat(f['fecha'])
            
            coleccion.insert_many(facturas)
            print(f"✓ {len(facturas)} facturas migradas con éxito.")
    except Exception as e:
        print(f"✗ Error al migrar facturas: {str(e)}")

def migrar_configuracion():
    print("⚙️ Migrando configuración...")
    if not os.path.exists("config.json"):
        print("⚠ No se encontró config.json")
        return

    try:
        with open("config.json", 'r', encoding='utf-8') as f:
            config = json.load(f)
            
        if config:
            coleccion = db.configuracion
            coleccion.delete_many({})
            coleccion.insert_one(config)
            print("✓ Configuración migrada con éxito.")
    except Exception as e:
        print(f"✗ Error al migrar configuración: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando migración a MongoDB Atlas...")
    migrar_productos()
    migrar_facturas()
    migrar_configuracion()
    print("✅ Proceso de migración finalizado.")
