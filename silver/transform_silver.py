import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import get_engine

# --------------------------------------------------------- #
#              LIMPIEZA Y NORMALIZACIÓN DE DATOS            #
# --------------------------------------------------------- #

def transform_silver():
    engine = get_engine()

    # Leer tablas desde bronze
    customers = pd.read_sql("SELECT * FROM customers", engine)
    products = pd.read_sql("SELECT * FROM products", engine)
    orders = pd.read_sql("SELECT * FROM orders", engine)

    # Normalizar columnas
    customers.columns = [c.strip().lower().replace(" ", "_") for c in customers.columns]
    products.columns = [c.strip().lower().replace(" ", "_") for c in products.columns]
    orders.columns = [c.strip().lower().replace(" ", "_") for c in orders.columns]

    # Eliminar filas con null en la PK y filas duplicadas
    customers = customers.dropna(subset=["customer_id"]).drop_duplicates()
    products = products.dropna(subset=["product_id"]).drop_duplicates()
    orders = orders.dropna(subset=["order_id"]).drop_duplicates(subset=["order_id", "product_id"]) # Elimina solo casos donde se repite exactamente el mismo producto en la misma orden

    # Convertir fechas
    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["ship_date"] = pd.to_datetime(orders["ship_date"])

    # Reemplazar NaN por 0, en caso de existir
    orders["sales"] = orders["sales"].fillna(0)
    orders["quantity"] = orders["quantity"].fillna(0)
    orders["discount"] = orders["discount"].fillna(0)
    orders["profit"] = orders["profit"].fillna(0)

    # Guardar tablas limpias en MySQL (silver)
    customers.to_sql("customers_silver", engine, if_exists="replace", index=False)
    products.to_sql("products_silver", engine, if_exists="replace", index=False)
    orders.to_sql("orders_silver", engine, if_exists="replace", index=False)

    print("✅ Tablas Silver listas en MySQL")

# Ejecuta solo si el archivo se corre directamente (y no cuando se importa como módulo en otro programa)
if __name__ == "__main__":
    transform_silver()