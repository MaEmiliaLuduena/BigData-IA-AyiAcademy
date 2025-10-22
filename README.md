# BigData & IA - Ayi Academy
# Proyecto Superstore – Arquitectura Medallón

Este proyecto implementa un flujo ETL basado en la arquitectura __Medallón (Bronze–Silver–Gold)__, utilizando el dataset __Superstore__, una tienda minorista en Estados Unidos, que vende productos de oficina, tecnología y mobiliario a clientes individuales y corporativos.

* __Bronze:__ ingestión de datos crudos y almacenamiento en MySQL.
* __Silver:__ limpieza, normalización y eliminación de duplicados.
* __Gold:__ preparación para análisis y visualización.

## Tecnologías usadas:

* __Python (Pandas, SQLAlchemy, PyMySQL)__
* __MySQL__
* __Matplotlib y Seaborn para visualización__

## Objetivo

Practicar conceptos de __Big Data & IA__ y demostrar la aplicación de pipelines de datos modernos con enfoque en __calidad y análisis__.

### 1. 📌 Requisitos previos

* Tener instalado Python 3.10+
* Tener instalado MySQL (con usuario y base creados)
* Git para clonar el repo


### 2. ⚙️ Instalación

#### Clonar el repositorio
git clone [https://github.com/tu-usuario/proyecto-superstore.git](https://github.com/MaEmiliaLuduena/BigData-IA-AyiAcademy.git)

cd proyecto-superstore

#### Crear entorno virtual
python -m venv venv

#### Activar entorno
venv\Scripts\activate   # En Windows
source venv/bin/activate  # En Linux/Mac

#### Instalar dependencias
pip install -r requirements.txt


### 3. 🛠️ Configuración de la base de datos

* Crear una base de datos MySQL vacía (ej: superstore_db)
* Editar el archivo db_connection.py con tus credenciales de MySQL

### 4. 🚀 Ejecución del pipeline

__1. Bronze (datos crudos)__
<br> python bronze/split_dataset.py  ---> Divide el dataset
<br> python bronze/load_bronze.py

__2. Silver (datos limpios)__
<br> python silver/transform_silver.py

__3. Gold (dataset final)__
<br> python gold/build_gold.py

__4. Visualización__
<br> python gold/visualize_gold.py


### 5. 📊 Visualización

Los gráficos se muestran en pantalla al ejecutar visualize_gold.py.
También se guardan como imágenes si descomentás las líneas correspondientes.

### 6. 📦 Dependencias

Todas las librerías necesarias están listadas en requirements.txt.
Si necesitás actualizarlo luego de instalar nuevas dependencias:
pip freeze > requirements.txt

