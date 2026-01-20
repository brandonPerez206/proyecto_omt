from flask import Flask
from flask_mail import Mail
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.registros_routes import registros_bp
from routes.usuarios_routes import usuarios_bp
from routes.historial_routes import historial_bp
from routes.setup_templates import ensure_templates_and_static


app = Flask(__name__)
app.secret_key = "admin123"

# Configuración del correo
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'brandonperez1209@gmail.com'
app.config['MAIL_PASSWORD'] = 'jlfimkkjnyalercq'



mail = Mail(app)

# Registro de las rutas
def register_routes(app: Flask):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(registros_bp)
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(historial_bp)

from routes import register_routes
if __name__ == '__main__':
    ensure_templates_and_static()
    register_routes(app)
    app.run(host='0.0.0.0', port=5000, debug=True)