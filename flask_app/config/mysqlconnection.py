import pymysql.cursors  # Utilizamos PyMySQL para interactuar con MySQL

# Clase que permite generar una instancia de conexión con la Base de Datos
class MySQLConnection:
    def __init__(self, db):
        # Establecemos la conexión con MySQL
        connection = pymysql.connect(
            host='localhost',
            user='root',      # Cambia si usas otro usuario
            password='root',  # Cambia si tu contraseña es distinta
            db=db,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True,
        )
        self.connection = connection  # Guardamos conexión activa

    # Método responsable de ejecutar consultas SQL
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                # Si viene "data", entonces mogrify arma la consulta con parámetros
                if data:
                    query = cursor.mogrify(query, data)
                    print("Running Query:", query)
                    cursor.execute(query, data)
                else:
                    # Si no hay parámetros, ejecutamos directamente
                    print("Running Query:", query)
                    cursor.execute(query)

                # Si la consulta es INSERT
                if query.lower().find("insert") >= 0:
                    self.connection.commit()  # Guardamos cambios
                    return cursor.lastrowid   # Regresamos ID generado

                # Si la consulta es SELECT
                elif query.lower().find("select") >= 0:
                    result = cursor.fetchall()  # Regresa lista de diccionarios
                    return result

                # Para UPDATE y DELETE
                else:
                    self.connection.commit()  # Guardamos cambios
                    return None

            except Exception as e:
                # Si algo falla, print del error y regresamos False
                print("ERROR en query_db:", e)
                return False


# Función para crear instancia de MySQLConnection apuntando a una BD específica
def connectToMySQL(db):
    return MySQLConnection(db)
