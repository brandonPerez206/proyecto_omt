from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask import send_file
import sqlite3, os
import pandas as pd


app = Flask(__name__)
app.secret_key = "admin123"



@app.route('/cambiar_contrasena/<int:user_id>', methods=['GET', 'POST'])
def cambiar_contrasena(user_id):
    # Solo el administrador puede acceder
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    # Obtener usuario por ID
    c.execute("SELECT id, usuario FROM usuarios WHERE id = ?", (user_id,))
    user = c.fetchone()

    if not user:
        conn.close()
        flash("❌ Usuario no encontrado.", "danger")
        return redirect(url_for('usuarios'))

    if request.method == 'POST':
        nueva_pass = request.form.get('nueva_pass')
        confirmar_pass = request.form.get('confirmar_pass')

        if not nueva_pass or not confirmar_pass:
            flash("⚠️ Debes completar ambos campos.", "warning")
        elif nueva_pass != confirmar_pass:
            flash("⚠️ Las contraseñas no coinciden.", "danger")
        else:
            hashed_pass = generate_password_hash(nueva_pass)
            c.execute("UPDATE usuarios SET password = ? WHERE id = ?", (hashed_pass, user_id))
            conn.commit()
            flash(f"✅ Contraseña actualizada para {user[1]}.", "success")
            conn.close()
            return redirect(url_for('usuarios'))

    conn.close()
    return render_template('cambiar_contrasena.html', user=user)



from flask_mail import Message
from flask_mail import Mail

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'brandonperez1209@gmail.com'
app.config['MAIL_PASSWORD'] = 'jlfimkkjnyalercq'  

mail = Mail(app)

@app.route('/solicitud_recuperacion', methods=['GET', 'POST'])
def solicitud_recuperacion():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        motivo = request.form.get('motivo')

        # Correo destino fijo
        destino = "brandonperez1209@gmail.com"  

        # Crear mensaje
        msg = Message  (
            subject="🔐 Solicitud de Restablecimiento de Contraseña",
            sender=app.config['MAIL_USERNAME'],
            recipients=[destino]
        )

        msg.body = f"""
        Se ha recibido una solicitud de restablecimiento de contraseña.

        👤 Nombre del trabajador: {nombre}
        📝 Motivo: {motivo}
        """
        mail.send(msg)
        flash('📩 Tu solicitud fue enviada correctamente. Pronto recibirás asistencia.', 'success')
        return redirect(url_for('login'))

    return render_template('solicitud_recuperacion.html')


# --- Inicializar base de datos ---

def init_db():
    if not os.path.exists("database.db"):
        with sqlite3.connect("database.db") as conn:
            conn.execute('''CREATE TABLE usuarios (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre TEXT,
                                usuario TEXT UNIQUE,
                                password TEXT
                            )''')
            conn.execute('''CREATE TABLE registros (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                tipo TEXT,
                                descripcion TEXT,
                                autor TEXT,
                                fecha TEXT,
                                hora TEXT
                            )''')
            # Crear un usuario admin por defecto
            conn.execute("INSERT INTO usuarios (nombre, usuario, password) VALUES (?, ?, ?)",
                         ("Administrador", "admin", "admin"))
            conn.commit()
init_db()

# --- Rutas principales ---
@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conn = sqlite3.connect('bitacoras.db')
        c = conn.cursor()
        c.execute("SELECT id, usuario, password, rol FROM usuarios WHERE usuario = ?", (usuario,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            session['usuario'] = user[1]
            session['rol'] = user[3]
            flash(f"👋 Bienvenido {user[1]}", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Usuario o contraseña incorrectos.", "danger")

    return render_template('login.html')



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    # Obtener los últimos 10 registros
    c.execute("SELECT id, fecha, hora, usuario, tipo, descripcion FROM registros ORDER BY id DESC LIMIT 10")
    ultimos = c.fetchall()

    conn.close()

    return render_template('dashboard.html', ultimos=ultimos, usuario=session['usuario'], rol=session['rol'])
from datetime import datetime

@app.route('/registros', methods=['GET', 'POST'])
def registros():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        usuario = session['usuario']
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        c.execute("INSERT INTO registros (usuario, tipo, descripcion, fecha, hora) VALUES (?, ?, ?, ?, ?)",
                  (usuario, tipo, descripcion, fecha, hora))
        conn.commit()

    c.execute("SELECT fecha, hora, usuario, tipo, descripcion FROM registros ORDER BY id DESC")
    lista_registros = c.fetchall()
    conn.close()

    return render_template('registros.html', registros=lista_registros, usuario=session['usuario'], rol=session['rol'])

    


@app.route('/usuarios', methods=['GET', 'POST'])
def usuarios():
    # Solo los administradores pueden acceder
    if 'usuario' not in session or session['rol'] != 'Administrador':
        return redirect(url_for('dashboard'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    

    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']
        rol = request.form['rol']

        # Verificar si el usuario ya existe
        c.execute("SELECT * FROM usuarios WHERE usuario = ?", (usuario,))
        existe = c.fetchone()

        if existe:
            # Mensaje de advertencia si ya existe
            flash(f"⚠️ El usuario '{usuario}' ya existe. Intente con otro nombre.", "error")
        else:
            # Crear usuario nuevo
            hashed_pass = generate_password_hash(password)
            c.execute("INSERT INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
                      (usuario, password, rol))
            conn.commit()
            flash(f"✅ Usuario '{usuario}' creado exitosamente.", "success")
        if 'usuario' not in session or session['rol'] != 'Administrador':
            return redirect(url_for('dashboard'))


    # Cargar todos los usuarios para mostrar en la tabla
    c.execute("SELECT id, usuario, rol FROM usuarios")
    usuarios = c.fetchall()
    conn.close()

    return render_template('usuarios.html', usuarios=usuarios)

    # Mostrar lista de usuarios
    c.execute("SELECT id, usuario, rol FROM usuarios")
    lista_usuarios = c.fetchall()
    conn.close()
    return render_template('usuarios.html', usuarios=lista_usuarios)

def init_registros():
    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registros (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT NOT NULL,
                    tipo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    fecha TEXT NOT NULL,
                    hora TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

init_registros()

init_db()

@app.route('/eliminar_registro/<int:id>', methods=['POST'])
def eliminar_registro(id):
    # Validar sesión activa
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    # Solo administradores pueden eliminar
    if session.get('rol') != 'Administrador':
        flash('No tienes permisos para eliminar registros.', 'danger')
        return redirect(url_for('historial'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("DELETE FROM registros WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Registro eliminado correctamente.', 'success')
    return redirect(url_for('historial'))

@app.route('/eliminar_usuario/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("DELETE FROM usuarios WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('usuarios'))

@app.route('/historial')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bitacoras.db')
    cursor = conn.cursor()

    # Filtrado opcional
    usuario = request.args.get('usuario')
    fecha = request.args.get('fecha')

    query = "SELECT * FROM registros WHERE 1=1"
    params = []

    if usuario:
        query += " AND usuario LIKE ?"
        params.append(f"%{usuario}%")
    if fecha:
        query += " AND fecha = ?"
        params.append(fecha)

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    registros = cursor.fetchall()
    conn.close()

    return render_template('historial.html', registros=registros)

@app.route('/exportar_bitacoras')
def exportar_bitacoras():
    # Conexión a la base de datos
    conn = sqlite3.connect('bitacoras.db')

    # Asegúrate de que el nombre de la tabla coincida (ajústalo si usas otro)
    df = pd.read_sql_query("SELECT * FROM registros ORDER BY id DESC", conn)
    conn.close()

    # Guardar el Excel en carpeta temporal dentro de static
    file_path = os.path.join('static', 'historial_completo.xlsx')
    df.to_excel(file_path, index=False)

    # Enviar archivo al navegador para descarga
    return send_file(file_path, as_attachment=True)

# --- Plantillas embebidas ---
@app.context_processor
def inject_templates():
    if not os.path.exists("templates"):
        os.makedirs("templates")
        # base.html
        with open("templates/base.html", "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='UTF-8'>
  <title>Bitácoras OMT Alico</title>
  <link rel='stylesheet' href='{{ url_for("static", filename="style.css") }}'>
</head>
<body>
  <div class='sidebar'>
    <h2>Bitácoras OMT Alico</h2>
    <a href='{{ url_for("dashboard") }}'>Inicio</a>
    <a href='{{ url_for("registros") }}'>Registros</a>
    <a href='{{ url_for("usuarios") }}'>Usuarios</a>
    <a href='{{ url_for("logout") }}' class='logout'>Cerrar sesión</a>
  </div>
  <div class='main'>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <div class='flash'>{{ messages[0] }}</div>
      {% endif %}
    {% endwith %}
    {% block content %}{% endblock %}
  </div>
</body>
</html>""")
        # login.html
        with open("templates/login.html", "w", encoding="utf-8") as f:
            f.write("""<!DOCTYPE html>
<html lang='es'>
<head>
  <meta charset='UTF-8'>
  <title>Iniciar Sesión</title>
  <link rel='stylesheet' href='{{ url_for("static", filename="style.css") }}'>
</head>
<body class='login-page'>
  <form method='POST' class='login-form'>
    <h2>Iniciar sesión</h2>
    <input type='text' name='usuario' placeholder='Usuario' required>
    <input type='password' name='password' placeholder='Contraseña' required>
    <button type='submit'>Entrar</button>
  </form>
</body>
</html>""")
        # dashboard.html
        with open("templates/dashboard.html", "w", encoding="utf-8") as f:
            f.write("""{% extends 'base.html' %}
{% block content %}
<h1>Bienvenido, {{ usuario }}</h1>
<p>Selecciona una opción del menú lateral para continuar.</p>
{% endblock %}""")
        # registros.html
        with open("templates/registros.html", "w", encoding="utf-8") as f:
            f.write("""{% extends 'base.html' %}
{% block content %}
<h1>Registros</h1>
<form method='POST' class='registro-form'>
  <select name='tipo' required>
    <option value=''>Seleccionar tipo</option>
    <option>Novedad</option>
    <option>Ingreso</option>
    <option>Salida</option>
    <option>Accidente</option>
  </select>
  <textarea name='descripcion' placeholder='Descripción...' required></textarea>
  <button type='submit'>Guardar</button>
</form>
<table>
  <tr><th>Tipo</th><th>Descripción</th><th>Autor</th><th>Fecha</th><th>Hora</th></tr>
  {% for r in registros %}
  <tr><td>{{r[1]}}</td><td>{{r[2]}}</td><td>{{r[3]}}</td><td>{{r[4]}}</td><td>{{r[5]}}</td></tr>
  {% endfor %}
</table>
{% endblock %}""")
        # usuarios.html
        with open("templates/usuarios.html", "w", encoding="utf-8") as f:
            f.write("""{% extends 'base.html' %}
{% block content %}
<h1>Usuarios</h1>
<form method='POST'>
  <input type='text' name='nombre' placeholder='Nombre completo' required>
  <input type='text' name='usuario' placeholder='Usuario' required>
  <input type='password' name='password' placeholder='Contraseña' required>
  <button type='submit'>Crear usuario</button>
</form>
<table>
  <tr><th>ID</th><th>Nombre</th><th>Usuario</th></tr>
  {% for u in usuarios %}
  <tr><td>{{u[0]}}</td><td>{{u[1]}}</td><td>{{u[2]}}</td></tr>
  {% endfor %}
</table>
{% endblock %}""")
    return {}

# --- CSS ---
if not os.path.exists("static"):
    os.makedirs("static")
    with open("static/style.css", "w", encoding="utf-8") as f:
        f.write("""body{margin:0;font-family:'Segoe UI',sans-serif;background:#f4f6f8;color:#333;}
.sidebar{position:fixed;left:0;top:0;width:220px;height:100vh;background:#14213d;color:white;display:flex;flex-direction:column;padding:20px;}
.sidebar a{color:#fff;text-decoration:none;margin:10px 0;}
.sidebar a.logout{margin-top:auto;color:#e63946;}
.main{margin-left:240px;padding:20px;}
.login-page{display:flex;align-items:center;justify-content:center;height:100vh;background:#14213d;}
.login-form{background:white;padding:30px;border-radius:8px;display:flex;flex-direction:column;gap:10px;}
button{background:#14213d;color:white;border:none;padding:10px;cursor:pointer;}
.flash{background:#ffcc00;padding:8px;border-radius:5px;}""")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    rol TEXT NOT NULL
                )''')
    # Usuario admin por defecto
    c.execute("INSERT OR IGNORE INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
              ("admin", "admin", "Administrador"))
    conn.commit()
    conn.close()

init_db()

import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Crear base de datos si no existe
def init_db():
    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usuario TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    rol TEXT NOT NULL
                )''')
    # Usuario admin por defecto
    c.execute("INSERT OR IGNORE INTO usuarios (usuario, password, rol) VALUES (?, ?, ?)",
              ("admin", "admin", "Administrador"))
    conn.commit()
    conn.close()

import pandas as pd
from flask import send_file

