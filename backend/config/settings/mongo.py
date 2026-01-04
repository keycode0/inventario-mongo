from mongoengine import connect

def init_mongo():
    connect(
        db="inventario_db",
        host="mongo",
        port=27017,
        alias="default",
        serverSelectionTimeoutMS=1000,
        connectTimeoutMS=1000,
    )
