from flask import Blueprint, render_template, redirect, url_for, session
import sqlite3

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("SELECT id, fecha, hora, usuario, tipo, descripcion FROM registros ORDER BY id DESC LIMIT 10")
    ultimos = c.fetchall()
    conn.close()

    return render_template('dashboard.html', ultimos=ultimos, usuario=session['usuario'], rol=session['rol'])
