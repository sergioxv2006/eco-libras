from flask import Flask 
from .routes import rotas_principal
import os 

def criar_aplicacao(): 
    app = Flask(__name__)
    
    app.register_blueprint(rotas_principal)

    return app