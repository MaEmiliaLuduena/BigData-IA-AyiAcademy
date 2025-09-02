import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import get_engine

# ----------------------------------------------------- #
#                  CARGAR LOS CSV A MySQL               #
# ----------------------------------------------------- #

def load_bronze():
    # Llamar a la base de datos
    engine = get_engine()

    # Cargar los CSV ya divididos
    df_customers = pd.read_csv("bronze/Customers.csv")
    df_products = pd.read_csv("bronze/Products.csv")
    df_orders = pd.read_csv("bronze/Orders.csv")

    # Subir a MySQL (reemplaza tablas si ya existen)
    df_customers.to_sql("customers", engine, if_exists="replace", index=False)
    df_products.to_sql("products", engine, if_exists="replace", index=False)
    df_orders.to_sql("orders", engine, if_exists="replace", index=False)

    print("✅ Tablas Bronze cargadas en MySQL")

# Ejecutar solo si el archivo se corre directamente (y no cuando se importa como módulo en otro programa)
if __name__ == "__main__":
    load_bronze()
