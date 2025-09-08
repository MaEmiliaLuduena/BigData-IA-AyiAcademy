import pandas as pd
import os # Gestiona automáticamente las diferencias entre sistemas operativos como '/' en Linux/macOS o '\' en Windows

# -------------------------------- #
#    DESCARGAR DATASET ORIGINAL    #
# -------------------------------- #
# Carpeta destino
data_dir = "data/raw/"
os.makedirs(data_dir, exist_ok=True)

# Descargar dataset de Kaggle
os.system(f'kaggle datasets download -d vivek468/superstore-dataset-final -p {data_dir} --unzip')

# Leer archivo descargado
file_path = os.path.join(data_dir, "Sample - Superstore.csv")
df = pd.read_csv(file_path, encoding="ISO-8859-1") # Utilizo encoding para poder leer el dataset. El original no está en UTF-8

print("Primeras filas del dataset:")
print(df.head())


# ------------------------------------------------------------- #
#    DIVIDIR DATASET ORIGINAL EN CUSTOMERS, PRODUCTS Y ORDERS   #
# ------------------------------------------------------------- #
# Customers
customers = df[[
    "Customer ID", "Customer Name", "Segment", "Country",
    "City", "State", "Postal Code", "Region"
]]

# Products
products = df[[
    "Product ID", "Category", "Sub-Category", "Product Name"
]]

# Orders
orders = df[[
    "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Product ID", "Sales", "Quantity", "Discount", "Profit"
]]

# Guardar datasets separados
customers.to_csv("bronze/Customers.csv", index=False)
products.to_csv("bronze/Products.csv", index=False)
orders.to_csv("bronze/Orders.csv", index=False)

print("✅ Datasets divididos en Customers, Products y Orders")