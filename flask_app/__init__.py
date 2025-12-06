from flask import Flask
from flask_bcrypt import Bcrypt

# Instancia principal de Flask
app = Flask(__name__)

# Clave secreta para las sesiones (puede ser cualquier string)
app.secret_key = "clave_secreta_voluntame_2025"

# Bcrypt para encriptar contraseñas
bcrypt = Bcrypt(app)