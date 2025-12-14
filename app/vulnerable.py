import psycopg2
import pymysql

# OJO: en compose usamos los nombres de servicio como host
pg = psycopg2.connect(
    host="postgres",
    dbname="postgres",
    user="postgres",
    password="postgres"
)

my = pymysql.connect(
    host="mysql",
    user="root",
    password="",
    database="tienda",
    autocommit=True
)

def buscar_usuario():
    nombre = input("Nombre a buscar en PostgreSQL: ")
    cur = pg.cursor()
    # ❌ Vulnerable a SQLi
    query = f"SELECT id, nombre, email FROM usuarios WHERE nombre = '{nombre}';"
    print(f"[DEBUG] Ejecutando: {query}")
    cur.execute(query)
    filas = cur.fetchall()
    print("Resultados:", filas)

def insertar_producto():
    nombre = input("Nombre del producto (MySQL): ")
    precio = input("Precio: ")
    cur = my.cursor()
    # ❌ Vulnerable a SQLi
    query = f"INSERT INTO productos (nombre, precio) VALUES ('{nombre}', {precio});"
    print(f"[DEBUG] Ejecutando: {query}")
    cur.execute(query)
    print("Producto insertado (si no ha petado).")

if __name__ == "__main__":
    print("Demo vulnerable. Opciones:")
    print("1) Buscar usuario (Postgres)")
    print("2) Insertar producto (MySQL)")
    op = input("Opción: ")
    if op == "1":
        buscar_usuario()
    elif op == "2":
        insertar_producto()
    else:
        print("Opción no válida.")
