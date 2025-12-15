import os
import sys
from decimal import Decimal, InvalidOperation

import psycopg2
import pymysql


def get_postgres_connection():
    return psycopg2.connect(
        host=os.getenv("PG_HOST", "postgres"),
        dbname=os.getenv("PG_DB", "postgres"),
        user=os.getenv("PG_APP_USER", "appuser"),
        password=os.getenv("PG_APP_PASS", "Fuerte#2025"),
    )


def get_mysql_connection():
    return pymysql.connect(
        host=os.getenv("MY_HOST", "mysql"),
        user=os.getenv("MY_APP_USER", "app"),
        password=os.getenv("MY_APP_PASS", "Fuerte#2025"),
        database=os.getenv("MY_DB", "tienda"),
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor,
    )


def buscar_usuario_seguro(pg_conn):
    try:
        nombre = input("Nombre a buscar (seguro, PG): ").strip()
    except EOFError:
        print("\nEntrada no disponible. Saliendo.")
        sys.exit(0)
    if not nombre:
        print("Nombre vacío.")
        return
    with pg_conn.cursor() as cur:
        cur.execute("SELECT id, nombre, email FROM usuarios WHERE nombre = %s;", (nombre,))
        filas = cur.fetchall()
    if not filas:
        print("Sin resultados.")
    else:
        for fila in filas:
            print(f"[{fila[0]}] {fila[1]} <{fila[2]}>")


def insertar_producto_seguro(my_conn):
    try:
        nombre = input("Nombre del producto (seguro, MySQL): ").strip()
    except EOFError:
        print("\nEntrada no disponible. Saliendo.")
        sys.exit(0)
    if not nombre:
        print("Nombre vacío.")
        return
    try:
        precio_txt = input("Precio (número): ").strip()
    except EOFError:
        print("\nEntrada no disponible. Saliendo.")
        sys.exit(0)
    try:
        precio = Decimal(precio_txt)
    except (InvalidOperation, ValueError):
        print("Precio inválido.")
        return
    with my_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO productos (nombre, precio) VALUES (%s, %s);",
            (nombre, str(precio)),
        )
    print("Producto insertado de forma segura.")


def listar_productos_seguro(my_conn):
    with my_conn.cursor() as cur:
        cur.execute("SELECT id, nombre, precio FROM productos ORDER BY id;")
        filas = cur.fetchall()
    if not filas:
        print("No hay productos.")
    else:
        for fila in filas:
            print(f"[{fila['id']}] {fila['nombre']} - {fila['precio']}")


def main():
    try:
        pg_conn = get_postgres_connection()
        my_conn = get_mysql_connection()
    except Exception as exc:
        print(f"Error al conectar a las bases de datos: {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        while True:
            print("\nApp segura. Opciones:")
            print("1) Buscar usuario (Postgres)")
            print("2) Insertar producto (MySQL)")
            print("3) Listar productos (MySQL)")
            print("q) Salir")
            try:
                op = input("Opción: ").strip().lower()
            except EOFError:
                print("\nEntrada no disponible. Saliendo.")
                break

            if op == "1":
                buscar_usuario_seguro(pg_conn)
            elif op == "2":
                insertar_producto_seguro(my_conn)
            elif op == "3":
                listar_productos_seguro(my_conn)
            elif op in {"q", "quit", "exit"}:
                break
            else:
                print("Opción no válida.")
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario.")
    finally:
        pg_conn.close()
        my_conn.close()


if __name__ == "__main__":
    main()
