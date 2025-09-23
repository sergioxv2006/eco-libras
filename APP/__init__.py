from flask import Flask

from .routes import rotas_principal
from .extencoes import db, migrate
from .config import Configuracao
import os

def criar_aplicacao():
    app = Flask(__name__)
    app.config.from_object(Configuracao)
    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(rotas_principal)
    return app