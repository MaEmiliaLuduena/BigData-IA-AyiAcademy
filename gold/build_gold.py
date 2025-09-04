import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_connection import get_engine

# ------------------------------------------------------------- #
#                  TRANSFORMACIONES DE NEGOCIO                  #
# ------------------------------------------------------------- #

# Conexión a MySQL
engine = get_engine()

# Leer tablas Silver
customers = pd.read_sql("SELECT * FROM customers_silver", engine)
products = pd.read_sql("SELECT * FROM products_silver", engine)
orders = pd.read_sql("SELECT * FROM orders_silver", engine)


# ---------------------------------------- #
# 1. PRODUCTOS MÁS VENDIDOS POR CATEGORÍA  #
# ---------------------------------------- #

# Unir tablas Orders + Products
orders_products = orders.merge(products, on="product_id")

# Agrupar cantidad por categoría y productos
qty_by_product_cat = orders_products.groupby(
    ["category", "product_name"], as_index=False # evita que las columnas que utilizo dentro de groupby se utilicen como índice
    )["quantity"].sum()

# Ordenar primero por categoría y luego por cantidad
qty_by_product_cat_sorted = qty_by_product_cat.sort_values(
    ["category", "quantity"], ascending=[True, False]
)

# Top 5 de cada categoría
top_products = qty_by_product_cat_sorted.groupby("category").head(5).reset_index(drop=True) # restablece el índice y descarta el índice original sin añadirlo a una nueva columna

# Gráfico: 5 productos más vendidos por categoría
for category in top_products["category"].unique(): # no repite categorias
    subset = top_products[top_products["category"] == category]
    plt.figure(figsize=(8,5))
    plt.barh(subset["product_name"], subset["quantity"], color="skyblue")
    plt.title(f"Top 5 productos más vendidos - {category}")
    plt.xlabel("Cantidad vendida")
    plt.gca().invert_yaxis() # invierto los ejes
    # Guardar imagen
    # plt.savefig(f"top_productos_{category}.png", dpi=300, bbox_inches="tight")
    plt.show()

# Guardar tabla 'Top Productos por Categoria' en BD
top_products.to_sql("kpi_top_products_by_category", engine, if_exists="replace", index=False)


# ------------------------ #
# 2. PRODUCTOS SIN VENTAS  #
# ------------------------ #

# Productos vendidos
sold_products = orders["product_id"].unique() # guarda productos vendidos sin repetirlos

# Productos sin ventas
unsold_products = products[~products["product_id"].isin(sold_products)] # productos que no aparecen en orders

# Conteo por categoría (incluyendo categorías con 0 ventas)
all_categories = products["category"].dropna().drop_duplicates().sort_values()

# Cantidad de productos por categoría sin ventas
cat_counts = unsold_products["category"].value_counts().reindex(all_categories, fill_value=0)

# Gráfico: cantidad por categoría
plt.figure(figsize=(6,4))
plt.bar(cat_counts.index, cat_counts.values)
plt.title("Productos sin ventas por categoría")
plt.xlabel("Categoría")
plt.ylabel("Cantidad de productos sin ventas")
# Guargar imagen
# plt.savefig("productos_sin_ventas.png", dpi=300, bbox_inches="tight")
plt.show()

# Guardo tabla 'Productos No Vendidos' en BD
unsold_products.to_sql("kpi_unsold_products", engine, if_exists="replace", index=False)

# Mensaje informativo en consola
if unsold_products.empty:
    print("✅ No hay productos sin ventas")
else:
    print(f"Encontrados {len(unsold_products)} productos sin ventas.")


# ------------------------------- #
# 3. CIUDADES CON MAYOR GANANCIA  #
# ------------------------------- #

# Unir tablas Orders + Customers
orders_customers = orders.merge(customers, on="customer_id")

# Ganancia por ciudad
profit_by_city = orders_customers.groupby("city", as_index=False)["profit"].sum()

# Top 10 ciudades
top_cities = profit_by_city.sort_values("profit", ascending=False).head(10)

# Gráfico
plt.figure(figsize=(10,6))
sns.barplot(
    data=top_cities.sort_values("profit", ascending=False),
    x="profit", y="city", hue="city",
    palette="Blues_r", legend=False
)
plt.title("Top 10 ciudades con mayor ganancia")
plt.xlabel("Ganancia total")
plt.ylabel("Ciudad")
# Guargar imagen
# plt.savefig("ciudades_mayor_ganancia.png", dpi=300, bbox_inches="tight")
plt.show()

# Guardo tabla 'Top Ciudades Mayor Ganancia' en BD
top_cities.to_sql("kpi_top_cities", engine, if_exists="replace", index=False)


# ------------------------------------ #
# 4. CANTIDAD DE VENTAS POR CATEGORÍA  #
# ------------------------------------ #

# Gráfico: Distribución cantidad de ventas de productos en cada categoría.
plt.figure(figsize=(8,6))
sns.boxplot(
    data=qty_by_product_cat, # llamo la variable creada en la transformación 1.
    x="category", y="quantity", hue="category", palette="Set2",
)
plt.title("Distribución de cantidad de ventas por categoría")
plt.xlabel("Categoría")
plt.ylabel("Cantidad de ventas")
# Guargar imagen
# plt.savefig("cantidad_de_ventas.png", dpi=300, bbox_inches="tight")
plt.show()

# Guardo tabla 'Cantidad de Ventas por Categoría' en BD
qty_by_product_cat.to_sql("kpi_qty_by_category", engine, if_exists="replace", index=False)


# --------------------------------------- #
# 5. CLIENTES MÁS RENTABLES POR SEGMENTO  #
# --------------------------------------- #

# Agrupar Ganancia por Segmento y Nombre de cliente
profit_by_customer_segment = orders_customers.groupby(
    ["segment", "customer_name"], as_index=False
)["profit"].sum()

# Ordenar primero por Segmento y luego por Ganancia
profit_by_segment_custName_sorted = profit_by_customer_segment.sort_values(
    ["segment", "profit"], ascending=[True, False]
)

# Top 5 por segmento
top_customers = profit_by_segment_custName_sorted.groupby("segment").head(5).reset_index(drop=True)

# Gráficos por segmento
for segment in top_customers["segment"].unique():
    subset = top_customers[top_customers["segment"] == segment]
    plt.figure(figsize=(8,5))
    plt.barh(subset["customer_name"], subset["profit"], color="orange")
    plt.title(f"Top clientes más rentables - {segment}")
    plt.xlabel("Ganancia total")
    plt.gca().invert_yaxis()
    # Guardar imagen
    # plt.savefig("clientes_rentables.png", dpi=300, bbox_inches="tight")
    plt.show()

# Guardo tabla 'Clientes Más Rentables por Segmento' en BD
top_customers.to_sql("kpi_top_customers", engine, if_exists="replace", index=False)

# ------------------------------- #
# 6. EVOLUCIÓN DE VENTAS POR AÑO  #
# ------------------------------- #

# Agregar columna Año
orders["year"] = orders["order_date"].dt.year

# Fusionar pedidos con productos para obtener la columna "Categoría".
orders_with_category = orders.merge(products[["product_id", "category"]], on="product_id")

# Ventas por Año y Categoría
sales_by_year = orders_with_category.groupby(["year", "category"])["sales"].sum().reset_index()

# Gráfico lineplot
plt.figure(figsize=(8,5))
sns.lineplot(data=sales_by_year, x="year", y="sales", marker="o", linewidth=2, hue="category")
plt.title("Evolución de Ventas por Año según Categoría", fontsize=14)
plt.xlabel("Año")
plt.ylabel("Ventas Totales")
plt.xticks(sales_by_year["year"])
plt.grid(True, linestyle="--", alpha=0.6)
# Guargar imagen
# plt.savefig("evolucion_ventas_x_anio.png", dpi=300, bbox_inches="tight")
plt.show()

# Guardo tabla 'Evolución de Ventas por Año' en BD
sales_by_year.to_sql("kpi_sales_by_year", engine, if_exists="replace", index=False)


# ------------------------------- #
# 7. CORRELACIÓN ENTRE VARIABLES  #
# ------------------------------- #

# Selección de variables numéricas
num_vars = orders[["sales", "quantity", "discount", "profit"]]

# Matriz de correlación
corr_matrix = num_vars.corr()

# Gráfico heatmap
plt.figure(figsize=(6,5))
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", center=0, linewidths=0.5, fmt=".2f")
plt.title("Mapa de Correlación entre Variables Numéricas", fontsize=14)
# Guargar imagen
# plt.savefig("correlacion_variables.png", dpi=300, bbox_inches="tight")
plt.show()

# Guardo tabla 'Correlación de Variables Numéricas' en BD
corr_matrix.to_sql("kpi_correlation_matrix", engine, if_exists="replace", index=False)