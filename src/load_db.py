import psycopg2
from psycopg2.extras import execute_values

def insert_data(data):
    if not data:
        print("No hay datos para insertar.")
        return

    conn = None
    cur = None

    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='megabus12345',
            host='127.0.0.1',
            port='5432'
        )
        cur = conn.cursor()

        # Eliminar datos antes de insertar para actualizar todos los datos
        cur.execute("DELETE FROM coins;")

        # Insertar los nuevos datos
        rows = [(d['id'], d['name'], d['symbol'], d['current_price'], d['market_cap']) for d in data]

        query = """
        INSERT INTO coins (id, name, symbol, current_price, market_cap)
        VALUES %s
        """

        execute_values(cur, query, rows)
        conn.commit()
        print("Datos insertados correctamente.")
    except Exception as e:
        print(f"Error al insertar en la base de datos: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
