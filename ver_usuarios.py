import sqlite3

conn = sqlite3.connect('bitacoras.db')
c = conn.cursor()

c.execute("SELECT id, usuario, password, rol FROM usuarios")
usuarios = c.fetchall()

for u in usuarios:
    print(f"ID: {u[0]} | Usuario: {u[1]} | Contraseña: {u[2]} | Rol: {u[3]}")

conn.close()
