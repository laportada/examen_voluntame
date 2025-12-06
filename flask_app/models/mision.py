from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date

DB = "voluntariado_schema"


class Mision:
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.fecha = data["fecha"]
        self.voluntarios_necesarios = data["voluntarios_necesarios"]
        self.descripcion = data["descripcion"]
        self.usuario_id = data["usuario_id"]
        self.creador_nombre = data.get("creador_nombre", "")
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ----------------- CREATE -----------------
    @classmethod
    def guardar(cls, data):
        query = """
            INSERT INTO misiones (nombre, fecha, voluntarios_necesarios, descripcion, usuario_id)
            VALUES (%(nombre)s, %(fecha)s, %(voluntarios_necesarios)s, %(descripcion)s, %(usuario_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)

    # ----------------- READ -----------------
    @classmethod
    def get_por_id(cls, data):
        query = """
            SELECT m.*, CONCAT(u.nombre) AS creador_nombre
            FROM misiones m
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.id = %(id)s;
        """
        resultado = connectToMySQL(DB).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def get_todas_futuras_con_conteo(cls):
        """Trae todas las misiones futuras con el nombre del creador."""
        query = """
            SELECT m.*, CONCAT(u.nombre) AS creador_nombre
            FROM misiones m
            JOIN usuarios u ON m.usuario_id = u.id
            WHERE m.fecha >= CURDATE()
            ORDER BY m.fecha ASC;
        """
        resultados = connectToMySQL(DB).query_db(query)
        misiones = []
        if resultados:
            for fila in resultados:
                misiones.append(cls(fila))
        return misiones

    # ----------------- UPDATE -----------------
    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE misiones
            SET nombre = %(nombre)s,
                fecha = %(fecha)s,
                voluntarios_necesarios = %(voluntarios_necesarios)s,
                descripcion = %(descripcion)s
            WHERE id = %(id)s;
        """
        return connectToMySQL(DB).query_db(query, data)

    # ----------------- DELETE -----------------
    @classmethod
    def eliminar(cls, data):
        """Elimina una misión por id (primero borra voluntarios relacionados)."""
        # OJO: nombre correcto de la tabla intermedia = voluntarios_misiones
        query_vol = "DELETE FROM voluntarios_misiones WHERE mision_id = %(id)s;"
        connectToMySQL(DB).query_db(query_vol, data)

        query = "DELETE FROM misiones WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

    # ----------------- VALIDACIÓN -----------------
    @staticmethod
    def validar_mision(form):
        es_valido = True

        nombre = form.get("nombre", "").strip()
        fecha_str = form.get("fecha", "")
        voluntarios = form.get("voluntarios_necesarios", "")
        descripcion = form.get("descripcion", "").strip()

        if len(nombre) < 2:
            flash("El nombre de la misión debe tener al menos 2 caracteres", "mision")
            es_valido = False

        if descripcion == "":
            flash("La descripción no puede estar vacía", "mision")
            es_valido = False

        # Fecha
        if fecha_str == "":
            flash("Debes ingresar una fecha", "mision")
            es_valido = False
        else:
            try:
                año, mes, dia = map(int, fecha_str.split("-"))
                fecha_form = date(año, mes, dia)
                if fecha_form < date.today():
                    flash("La fecha no puede ser en el pasado", "mision")
                    es_valido = False
            except ValueError:
                flash("Formato de fecha inválido", "mision")
                es_valido = False

        # Voluntarios necesarios
        try:
            v = int(voluntarios)
            if v < 2 or v > 20:
                flash("Voluntarios necesarios debe estar entre 2 y 20", "mision")
                es_valido = False
        except ValueError:
            flash("Voluntarios necesarios debe ser un número", "mision")
            es_valido = False

        return es_valido

    # ----------------- RELACIÓN USUARIOS-MISIONES -----------------
    @classmethod
    def obtener_ids_misiones_usuario(cls, data):
        """Ids de misiones en las que el usuario ya es voluntario."""
        query = """
            SELECT mision_id
            FROM voluntarios_misiones
            WHERE usuario_id = %(usuario_id)s;
        """
        filas = connectToMySQL(DB).query_db(query, data)
        if not filas:
            return []
        return [f["mision_id"] for f in filas]

    @classmethod
    def obtener_voluntarios_de_mision(cls, data):
        """Lista de usuarios que se han inscrito a una misión."""
        query = """
            SELECT u.*
            FROM voluntarios_misiones vm
            JOIN usuarios u ON vm.usuario_id = u.id
            WHERE vm.mision_id = %(mision_id)s;
        """
        return connectToMySQL(DB).query_db(query, data) or []

    @classmethod
    def usuario_es_voluntario(cls, data):
        """True/False si el usuario ya se inscribió en esa misión."""
        query = """
            SELECT * FROM voluntarios_misiones
            WHERE usuario_id = %(usuario_id)s AND mision_id = %(mision_id)s;
        """
        filas = connectToMySQL(DB).query_db(query, data)
        return bool(filas)

    @classmethod
    def agregar_voluntario(cls, data):
        query = """
            INSERT INTO voluntarios_misiones (usuario_id, mision_id)
            VALUES (%(usuario_id)s, %(mision_id)s);
        """
        return connectToMySQL(DB).query_db(query, data)
