import os

def ensure_templates_and_static():
    """Crea automáticamente las plantillas y el CSS si no existen."""

    # --- Crear carpeta templates ---
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

    # --- Crear carpeta static ---
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
