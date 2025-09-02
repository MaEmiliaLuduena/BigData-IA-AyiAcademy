# Conexión a MySQL con SQLAlchemy
from sqlalchemy import create_engine

def get_engine():
    user = "root"
    password = "1234"
    host = "localhost"
    port = "3306"
    db = "superstore_db"
    
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}")
    return engine
