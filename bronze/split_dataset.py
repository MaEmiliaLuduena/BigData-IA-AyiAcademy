import pandas as pd
import os # Gestiona automáticamente las diferencias entre sistemas operativos como '/' en Linux/macOS o '\' en Windows

# ----------------------------------------------------------------- #
#    DIVIDIR EL DATASET ORIGINAL A Customers, Products y Orders    #
# ----------------------------------------------------------------- #

# Ruta al dataset original
RAW_PATH = os.path.join("data", "raw", "Sample_Superstore.csv")

# Cargar dataset original
df = pd.read_csv(RAW_PATH, encoding="ISO-8859-1")

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