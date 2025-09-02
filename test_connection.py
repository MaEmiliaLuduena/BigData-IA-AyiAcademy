import pymysql

# Pruebo la conexión con la base de datos
try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="1234",
        database="superstore_db",
        port=3306
    )
    print("✅ Conectado a MySQL correctamente")
except Exception as e:
    print("❌ Error al conectar:", e)
finally:
    if 'conn' in locals() and conn.open:
        conn.close()