from flask import Flask

# Importamos las rutas (blueprints)
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.registros_routes import registros_bp
from routes.usuarios_routes import usuarios_bp
from routes.historial_routes import historial_bp


def register_routes(app: Flask):
    """
    Función para registrar todas las rutas (blueprints) en la app principal.
    """
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registros_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(historial_bp)