# Conexión a MySQL con SQLAlchemy
from sqlalchemy import create_engine

def get_engine():
    # Completar con los datos de tu bd
    user = ""
    password = ""
    host = ""
    port = ""
    db = "superstore_db"
    
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
    return engine
