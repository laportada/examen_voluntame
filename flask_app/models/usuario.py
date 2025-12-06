from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import bcrypt

# Nombre de la base de datos que creamos en MySQL
DB = "voluntariado_schema"


class Usuario:
    # Constructor: mapea una fila de la tabla usuarios a un objeto
    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # ----------------- CREATE -----------------
    @classmethod
    def guardar(cls, data):
        """Inserta un nuevo usuario en la BD.

        data debe contener: nombre, apellido, email, password (hash)
        """
        query = (
            "INSERT INTO usuarios (nombre, apellido, email, password) "
            "VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        )
        return connectToMySQL(DB).query_db(query, data)

    # ----------------- READ -----------------
    @classmethod
    def get_por_email(cls, data):
        """Busca un usuario por email. Regresa un objeto Usuario o None."""
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL(DB).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    @classmethod
    def get_por_id(cls, data):
        """Busca un usuario por id. Regresa un objeto Usuario o None."""
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        resultado = connectToMySQL(DB).query_db(query, data)
        if not resultado:
            return None
        return cls(resultado[0])

    # ----------------- VALIDACIONES -----------------
    @staticmethod
    def validar_registro(form):
        """Valida los datos del formulario de registro (lado servidor)."""
        es_valido = True

        nombre = form.get("nombre", "").strip()
        apellido = form.get("apellido", "").strip()
        email = form.get("email", "").strip()
        password = form.get("password", "")
        confirm = form.get("confirm_password", "")

        # Nombre
        if len(nombre) < 2:
            flash("El nombre debe tener al menos 2 caracteres", "register")
            es_valido = False

        # Apellido
        if len(apellido) < 2:
            flash("El apellido debe tener al menos 2 caracteres", "register")
            es_valido = False

        # Email con formato simple y sin repetir
        if "@" not in email or "." not in email:
            flash("E-mail no tiene un formato válido", "register")
            es_valido = False
        else:
            usuario = Usuario.get_por_email({"email": email})
            if usuario:
                flash("El e-mail ya está registrado", "register")
                es_valido = False

        # Contraseña mínimo 8 caracteres
        if len(password) < 8:
            flash("La contraseña debe tener al menos 8 caracteres", "register")
            es_valido = False

        # Confirmación coincide
        if password != confirm:
            flash("La contraseña y la confirmación no coinciden", "register")
            es_valido = False

        return es_valido

    @staticmethod
    def validar_login(form):
        """Valida los datos del login.

        Si todo está OK, regresa el objeto Usuario.
        Si algo falla, regresa False.
        """
        email = form.get("email", "").strip()
        password = form.get("password", "")

        usuario_en_bd = Usuario.get_por_email({"email": email})

        if not usuario_en_bd:
            flash("E-mail no está registrado", "login")
            return False

        if not bcrypt.check_password_hash(usuario_en_bd.password, password):
            flash("Contraseña incorrecta", "login")
            return False

        return usuario_en_bd
