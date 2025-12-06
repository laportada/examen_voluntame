from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.mision import Mision
from flask_app.models.usuario import Usuario
from datetime import date


# ------------ DASHBOARD (Página principal) ------------
@app.route("/dashboard")
def dashboard():
    # Verificamos que haya un usuario en sesión
    if "usuario_id" not in session:
        return redirect("/")

    # Traemos al usuario desde la BD (por si queremos mostrar más datos)
    usuario = Usuario.get_por_id({"id": session["usuario_id"]})

    # Traemos todas las misiones futuras, ordenadas por fecha (BONUS)
    misiones = Mision.get_todas_futuras_con_conteo()

    # IDs de misiones en las que el usuario ya es voluntario
    ids_misiones_voluntario = Mision.obtener_ids_misiones_usuario(
        {"usuario_id": session["usuario_id"]}
    )

    hoy = date.today()

    return render_template(
        "dashboard.html",
        usuario=usuario,
        misiones=misiones,
        ids_misiones_voluntario=ids_misiones_voluntario,
        hoy=hoy,
    )


# ------------ FORMULARIO NUEVA MISION ------------
@app.route("/misiones/nueva")
def nueva_mision():
    # Solo usuarios logueados
    if "usuario_id" not in session:
        return redirect("/")
    return render_template("nueva_mision.html")


# ------------ CREAR MISION (POST) ------------
@app.route("/misiones/crear", methods=["POST"])
def crear_mision():
    if "usuario_id" not in session:
        return redirect("/")

    # Validar formulario
    if not Mision.validar_mision(request.form):
        # Si hay errores, regresamos al formulario
        return redirect("/misiones/nueva")

    data = {
        "nombre": request.form["nombre"],
        "fecha": request.form["fecha"],
        "voluntarios_necesarios": request.form["voluntarios_necesarios"],
        "descripcion": request.form["descripcion"],
        "usuario_id": session["usuario_id"],
    }

    Mision.guardar(data)
    return redirect("/dashboard")


# ------------ FORMULARIO EDITAR MISION ------------
@app.route("/misiones/editar/<int:id>")
def editar_mision(id):
    if "usuario_id" not in session:
        return redirect("/")

    mision = Mision.get_por_id({"id": id})
    if not mision:
        return redirect("/dashboard")

    # BONUS: impedir que otro usuario edite una misión que no creó
    if mision.usuario_id != session["usuario_id"]:
        return redirect("/dashboard")

    return render_template("editar_mision.html", mision=mision)


# ------------ ACTUALIZAR MISION (POST) ------------
@app.route("/misiones/actualizar/<int:id>", methods=["POST"])
def actualizar_mision(id):
    if "usuario_id" not in session:
        return redirect("/")

    mision = Mision.get_por_id({"id": id})
    if not mision:
        return redirect("/dashboard")

    # BONUS: impedir que otro usuario edite una misión que no creó
    if mision.usuario_id != session["usuario_id"]:
        return redirect("/dashboard")

    # Validar formulario
    if not Mision.validar_mision(request.form):
        return redirect(f"/misiones/editar/{id}")

    data = {
        "id": id,
        "nombre": request.form["nombre"],
        "fecha": request.form["fecha"],
        "voluntarios_necesarios": request.form["voluntarios_necesarios"],
        "descripcion": request.form["descripcion"],
    }

    Mision.actualizar(data)
    return redirect("/dashboard")


# ------------ BORRAR MISION ------------
@app.route("/misiones/borrar/<int:id>")
def borrar_mision(id):
    # Solo usuarios con sesión
    if "usuario_id" not in session:
        return redirect("/")

    # Traemos la misión
    mision = Mision.get_por_id({"id": id})
    if not mision:
        # Si no existe, volvemos al dashboard
        return redirect("/dashboard")

    # Solo el líder puede borrar su misión
    if mision.usuario_id != session["usuario_id"]:
        return redirect("/dashboard")

    # Eliminamos de la BD
    Mision.eliminar({"id": id})

    # Volvemos al dashboard
    return redirect("/dashboard")


# ------------ VER MISION ------------
@app.route("/misiones/ver/<int:id>")
def ver_mision(id):
    if "usuario_id" not in session:
        return redirect("/")

    mision = Mision.get_por_id({"id": id})
    if not mision:
        return redirect("/dashboard")

    usuario = Usuario.get_por_id({"id": session["usuario_id"]})
    voluntarios = Mision.obtener_voluntarios_de_mision({"mision_id": id})
    es_voluntario = Mision.usuario_es_voluntario(
        {"usuario_id": session["usuario_id"], "mision_id": id}
    )

    hoy = date.today()

    return render_template(
        "ver_mision.html",
        mision=mision,
        usuario=usuario,
        voluntarios=voluntarios,
        es_voluntario=es_voluntario,
        hoy=hoy,
    )


# ------------ VOLUNTAME (AGREGAR VOLUNTARIO A MISIÓN) ------------
@app.route("/misiones/voluntame/<int:id>")
def voluntame(id):
    if "usuario_id" not in session:
        return redirect("/")

    mision = Mision.get_por_id({"id": id})
    if not mision:
        return redirect("/dashboard")

    hoy = date.today()

    # BONUS: no permitir sumarse a misiones pasadas
    if mision.fecha < hoy:
        return redirect("/dashboard")

    data = {
        "usuario_id": session["usuario_id"],
        "mision_id": id,
    }

    # Solo agregamos si aún no es voluntario
    if not Mision.usuario_es_voluntario(data):
        Mision.agregar_voluntario(data)

    return redirect(f"/misiones/ver/{id}")
