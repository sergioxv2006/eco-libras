from flask import Flask
import os
from .extencoes import db
from flask_migrate import Migrate
from .routes_principal import rotas_principal
from .routes_admin import rotas_admin
from .auth_routes import rotas_auth

def create_app(config_object=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Database configuration with absolute path
    db_path = os.path.join(app.instance_path, 'data_bank.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "change-me-in-production")

    if config_object:
        app.config.from_object(config_object)

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(rotas_principal)
    app.register_blueprint(rotas_admin)
    app.register_blueprint(rotas_auth)

    # Add debug logging
    if app.debug:
        @app.after_request
        def log_response(response):
            app.logger.debug(f"Status: {response.status}")
            app.logger.debug(f"Headers: {response.headers}")
            return response

    return app