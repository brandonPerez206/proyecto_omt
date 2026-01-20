from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from datetime import datetime

registros_bp = Blueprint('registros', __name__, url_prefix='/registros')

@registros_bp.route('/', methods=['GET', 'POST'])
def registros():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()

    # Registrar nueva entrada
    if request.method == 'POST':
        tipo = request.form['tipo']
        descripcion = request.form['descripcion']
        usuario = session['usuario']
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")

        c.execute("INSERT INTO registros (usuario, tipo, descripcion, fecha, hora) VALUES (?, ?, ?, ?, ?)",
                  (usuario, tipo, descripcion, fecha, hora))
        conn.commit()
        flash("Registro guardado correctamente ", "success")

    # Mostrar registros
    c.execute("SELECT fecha, hora, usuario, tipo, descripcion FROM registros ORDER BY id DESC")
    lista_registros = c.fetchall()
    conn.close()

    return render_template('registros.html', registros=lista_registros, usuario=session['usuario'], rol=session['rol'])


@registros_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(id):
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    if session.get('rol') != 'Administrador':
        flash('No tienes permisos para eliminar registros.', 'danger')
        return redirect(url_for('historial.historial'))

    conn = sqlite3.connect('bitacoras.db')
    c = conn.cursor()
    c.execute("DELETE FROM registros WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    flash('Registro eliminado correctamente.', 'success')
    return redirect(url_for('historial.historial'))
