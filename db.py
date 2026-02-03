"""
Módulo central para la conexión a MongoDB Atlas.
"""

import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# URI de conexión correjida
MONGODB_URI = "mongodb+srv://BrianGX:1234567890@cluster0.gkk9fnb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "SistemaFacturacion"

class Database:
    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                # Inicializar el cliente
                cls._client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
                cls._db = cls._client[DB_NAME]
                
                # Probar conexión
                cls._client.admin.command('ping')
                print("✓ Conexión exitosa a MongoDB Atlas")
            except Exception as e:
                print(f"✗ Error al conectar a MongoDB Atlas: {str(e)}")
                raise e
        return cls._instance

    @property
    def db(self):
        return self._db

    def get_collection(self, name):
        return self._db[name]

# Instancia global para exportar
mongo_db = Database()
db = mongo_db.db
