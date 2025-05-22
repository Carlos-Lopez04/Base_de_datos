import pymysql
import pymongo

# Conexión a MySQL
mysq_com = pymysql.connect(host="localhost", user="root", passwd="12345678", database="pizza_ninja", port=3306, cursorclass=pymysql.cursors.DictCursor
)
print("Conexión exitosa a MySQL")

mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
mongo_db = mongo_client["pizza_ninjaBD"]
print("Conexión exitosa a MongoDB")

try:
    with mysq_com.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        table_column = f"Tables_in_{mysq_com.db.decode()}"
        tables = [row[table_column] for row in cursor.fetchall()]
    print(f"Se encontraron {len(tables)} tablas en la base de datos MySQL.")

    for table in tables:
        print(f"\nProcesando tabla: {table}...")
        with mysq_com.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table}")
            data = cursor.fetchall()
            if data:
                mongo_db[table].insert_many(data)
                print(f"Tabla '{table}' migrada con éxito. Total de registros: {len(data)}")
            else:
                print(f"Tabla '{table}' está vacía. No se migraron datos.")

except Exception as e:
    print(f"Error durante la migración: {e}")

finally:
    mysq_com.close()
    mongo_client.close()
    print("\nMigración finalizada y conexiones cerradas.")
