from flask import render_template, redirect, request, session
from flask_app import app, bcrypt
from flask_app.models.usuario import Usuario


# RUTA RAÍZ: muestra formulario de login y registro
@app.route("/")
def index():
    return render_template("index.html")


# ------------ REGISTRO ------------
@app.route("/registro", methods=["POST"])
def registro():
    # 1. Validar datos del formulario
    if not Usuario.validar_registro(request.form):
        # Si no es válido, volvemos a la página principal
        return redirect("/")

    # 2. Encriptar contraseña
    pw_hash = bcrypt.generate_password_hash(request.form["password"])

    # 3. Armar datos para guardar en BD
    data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "password": pw_hash,
    }

    # 4. Guardar en la BD
    nuevo_id = Usuario.guardar(data)

    # 5. Guardar datos básicos en sesión
    session["usuario_id"] = nuevo_id
    session["nombre"] = request.form["nombre"]

    # 6. Redirigir al dashboard
    return redirect("/dashboard")


# ------------ LOGIN ------------
@app.route("/login", methods=["POST"])
def login():
    # Validar login: si algo falla, regresa False y hace flash de errores
    usuario = Usuario.validar_login(request.form)
    if not usuario:
        return redirect("/")

    # Guardamos datos en sesión
    session["usuario_id"] = usuario.id
    session["nombre"] = usuario.nombre

    return redirect("/dashboard")


# ------------ LOGOUT ------------
@app.route("/logout")
def logout():
    # Limpiar la sesión
    session.clear()
    # Volver a la página de login/registro
    return redirect("/")
