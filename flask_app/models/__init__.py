from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.secret_key = "clave_2025_voluntame"  # puedes cambiarla

bcrypt = Bcrypt(app)