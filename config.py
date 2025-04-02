import psycopg2

def test_connection(db_name, user, password, host, port):
    """
    La función `test_connection` intenta establecer una conexión a una base de datos PostgreSQL 
    utilizando las credenciales proporcionadas y devuelve un valor booleano que indica éxito junto con un mensaje.

    :param db_name: El parámetro `db_name` es el nombre de la base de datos a la que desea conectarse. 
    Es un parámetro obligatorio para establecer una conexión a una base de datos PostgreSQL mediante psycopg2.

    :param user: El parámetro `user` de la función `test_connection` es el nombre de usuario utilizado 
    para autenticarse y conectarse a la base de datos. Normalmente es una cuenta de usuario con los permisos 
    necesarios para acceder a la base de datos especificada por `db_name`.

    :param password: El parámetro `password` de esta función se utiliza para proporcionar la contraseña del usuario 
    de la base de datos al establecer una conexión con la base de datos PostgreSQL.

    :param host: El parámetro `host` de la función `test_connection` se refiere al nombre de host o la dirección 
    IP del servidor donde se aloja la base de datos. Esta es la ubicación donde se ejecuta y se puede acceder al servidor 
    de la base de datos. Se utiliza para establecer una conexión con el servidor de la base de datos.

    :param port: El parámetro `port` de la función `test_connection` se refiere al número de puerto en el que el servidor 
    de la base de datos escucha las conexiones. Normalmente, es un valor numérico que especifica el punto final de comunicación 
    del servidor de la base de datos. Por ejemplo, el puerto predeterminado para PostgreSQL es 5432.

    :return: La función `test_connection` devuelve una tupla con dos valores. El primer valor es un booleano que indica si la 
    conexión se realizó correctamente (Verdadero si es correcta, Falso si es incorrecta). El segundo valor es un mensaje de cadena 
    que proporciona información sobre el estado de la conexión (ya sea "Conexión exitosa" si la conexión es correcta o un mensaje 
    de error si la conexión falló).
    """
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=user, password=password, host=host, port=port
        )
        conn.close()
        return True, "Conexión exitosa"
    except Exception as e:
        return False, str(e)
    
def get_tables(db_name, user, password, host, port):
    """
    La función `get_tables` se conecta a una base de datos PostgreSQL y recupera las tablas junto con su primer atributo 
    en el esquema "public".

    :param db_name: El parámetro `db_name` de la función `get_tables` representa el nombre de la base de datos a la que se 
    desea conectar para recuperar información sobre las tablas y su primer atributo. Este parámetro debe ser una cadena que 
    especifique el nombre de la base de datos en el servidor PostgreSQL.

    :param user: El parámetro `user` de la función `get_tables` representa el nombre de usuario utilizado para autenticarse y 
    conectarse a la base de datos especificada por `db_name`. Este nombre de usuario debe tener los permisos necesarios para 
    acceder a la base de datos y recuperar información sobre sus tablas y columnas.

    :param password: El parámetro `password` de la función `get_tables` se utiliza para proporcionar la contraseña del usuario de
    la base de datos al establecer una conexión. Esta contraseña es necesaria para autenticar al usuario y acceder a la base de 
    datos especificada. Asegúrese de proporcionar la contraseña correcta para el usuario especificado.

    :param host: El parámetro `host` de la función `get_tables` se refiere al nombre de host o la dirección IP del servidor de base de 
    datos donde se ejecuta la base de datos PostgreSQL. Esta es la ubicación desde donde se puede acceder a la base de datos a través 
    de la red. Podría ser una dirección IP (p. ej., '127.0.0').

    :param port: El parámetro `port` de la función `get_tables` se refiere al número de puerto en el que se ejecuta el servidor de base 
    de datos PostgreSQL. Este es el número de puerto que la función utilizará para establecer una conexión con el servidor de base de datos. 
    Normalmente, se establece en `5432` de forma predeterminada para los servidores PostgreSQL.

    :return: La función `get_tables` devuelve una lista de tuplas, cada una de las cuales contiene el nombre de una tabla y el
    nombre de su primer atributo (columna). Si se produce una excepción durante la ejecución de la función, se devuelve una lista vacía.
    """
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

def get_audit_table(db_name, user, password, host, port, table_name):
    """
    La función `get_audit_table` se conecta a una base de datos PostgreSQL, recupera datos de una tabla específica mediante una 
    función de descifrado y devuelve los resultados en un formato estructurado.

    :param db_name: El parámetro `db_name` de la función `get_tables` representa el nombre de la base de datos a la que se 
    desea conectar para recuperar información sobre las tablas y su primer atributo. Este parámetro debe ser una cadena que 
    especifique el nombre de la base de datos en el servidor PostgreSQL.

    :param user: El parámetro `user` de la función `get_tables` representa el nombre de usuario utilizado para autenticarse y 
    conectarse a la base de datos especificada por `db_name`. Este nombre de usuario debe tener los permisos necesarios para 
    acceder a la base de datos y recuperar información sobre sus tablas y columnas.

    :param password: El parámetro `password` de la función `get_tables` se utiliza para proporcionar la contraseña del usuario de
    la base de datos al establecer una conexión. Esta contraseña es necesaria para autenticar al usuario y acceder a la base de 
    datos especificada. Asegúrese de proporcionar la contraseña correcta para el usuario especificado.

    :param host: El parámetro `host` de la función `get_tables` se refiere al nombre de host o la dirección IP del servidor de base de 
    datos donde se ejecuta la base de datos PostgreSQL. Esta es la ubicación desde donde se puede acceder a la base de datos a través 
    de la red. Podría ser una dirección IP (p. ej., '127.0.0').

    :param port: El parámetro `port` de la función `get_tables` se refiere al número de puerto en el que se ejecuta el servidor de base 
    de datos PostgreSQL. Este es el número de puerto que la función utilizará para establecer una conexión con el servidor de base de datos. 
    Normalmente, se establece en `5432` de forma predeterminada para los servidores PostgreSQL.

    :param table_name: El parámetro `table_name` de la función `get_audit_table` es el nombre de la tabla de la base de datos de la que se 
    desean recuperar los datos.

    :return: La función `get_audit_table` devuelve una tupla con tres elementos:

    1. Un valor booleano que indica si la operación se realizó correctamente.

    2. Un diccionario que contiene las columnas y los datos recuperados de la tabla.

    3. Un mensaje que indica el estado de la operación (si los datos se obtuvieron correctamente o no).
    """
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
