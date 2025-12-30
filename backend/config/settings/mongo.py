from mongoengine import connect
import os

def init_mongo():
    connect(
        db=os.getenv("MONGO_DB", "inventario_db"),
        host=os.getenv("MONGO_HOST", "mongo"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER"),
        password=os.getenv("MONGO_PASSWORD"),
        authentication_source="admin"
    )
