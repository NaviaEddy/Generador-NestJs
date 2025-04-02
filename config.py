import json
import psycopg2

def test_connection(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        conn.close()
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)
    
def get_tables(db_name, user, password, host, port):
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()
        
        # Obtener las tablas y su primer atributo
        cur.execute(
            """
            SELECT table_name, column_name 
            FROM information_schema.columns 
            WHERE table_schema = 'public' AND ordinal_position = 1
            """
        )
        tables = [(row[0], row[1]) for row in cur.fetchall()]
        conn.close()
        return tables
    except Exception:
        return []
    
import psycopg2

def get_audit_table(db_name, user, password, host, port, table_name):
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        cur = conn.cursor()

        # Consulta para obtener todos los datos de la tabla en el esquema private
        query = f"SELECT * FROM private.decrypt_mirror_table('{table_name}', 'llave')"
        cur.execute(query)

        # Obtener los resultados
        rows = cur.fetchall()

        # Si hay datos, convertir JSONB a diccionarios
        if rows:
            conn.close()
            rows = [row[0] for row in rows]
            columns = list(rows[0].keys()) if rows else []
            data = [[row[col] for col in columns] for row in rows]
            result = {
                "columns": columns,
                "data": data
            }
            return True, result, 'Datos obtenidos correctamente'
        else:
            conn.close()
            return False, [], 'No hay datos'

    except Exception as e:
        print(f"Error al conectar o ejecutar la consulta: {e}")
        return False, [], []
