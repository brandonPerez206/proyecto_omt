import sqlite3
from werkzeug.security import generate_password_hash

# Conectar con la base de datos
conn = sqlite3.connect('bitacoras.db')
c = conn.cursor()

# Obtener todos los usuarios
c.execute("SELECT id, password FROM usuarios")
usuarios = c.fetchall()

# Hashear cada contraseña 
for u in usuarios:
    user_id, password = u
    if not password.startswith('pbkdf2:sha256:'):  # evita volver a hashear
        hashed = generate_password_hash(password)
        c.execute("UPDATE usuarios SET password = ? WHERE id = ?", (hashed, user_id))
        print(f" Usuario {user_id}: contraseña convertida")

conn.commit()
conn.close()
print("\n✅ Todas las contraseñas fueron hasheadas correctamente.")
