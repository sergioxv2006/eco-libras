from flask import Blueprint, render_template, request, redirect, url_for, current_app, send_from_directory
import os 
from werkzeug.utils import secure_filename

rotas_principal = Blueprint("principal", __name__)


# Rota principal (index)
@rotas_principal.route("/")
def pagina_inicial():
    return render_template("index.html")

# Rota para página de acessibilidade
@rotas_principal.route("/acessibilidade")
def pagina_acessibilidade():
    return render_template("acessibilidade.html")

# Rota para página de admin (se existir o template)
@rotas_principal.route("/admin")
def pagina_admin():
    return render_template("admin.html")