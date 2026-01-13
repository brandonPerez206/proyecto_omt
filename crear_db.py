import sqlite3

# Crear o conectar a la base de datos
conn = sqlite3.connect('bitacoras.db')
c = conn.cursor()

# Crear tabla de usuarios
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        contrasena TEXT NOT NULL,
        rol TEXT NOT NULL
    )
''')

# Crear tabla de registros (si aún no existe)
c.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        fecha TEXT,
        descripcion TEXT
    )
''')

# Crear usuario administrador por defecto
c.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
if not c.fetchone():
    c.execute('''
        INSERT INTO usuarios (nombre, usuario, password, rol)
        VALUES (?, ?, ?, ?)
    ''', ('Administrador', 'admin', 'admin', 'Administrador'))
    print("✅ Usuario 'admin' creado (usuario: admin / contraseña: admin)")
else:
    print("ℹ️ El usuario 'admin' ya existe")

conn.commit()
conn.close()
print("✅ Base de datos creada correctamente")

