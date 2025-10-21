import pymysql

# Pruebo la conexión con la base de datos
try:
    # Completar con los datos de tu bd
    conn = pymysql.connect(
        host="tu_host",
        user="tu_user",
        password="tu_password",
        database="superstore_db",
        port=tu_puerto
    )
    print("✅ Conectado a MySQL correctamente")
except Exception as e:
    print("❌ Error al conectar:", e)
finally:
    if 'conn' in locals() and conn.open:
        conn.close()
