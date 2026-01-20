from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
import sqlite3, os
import pandas as pd

historial_bp = Blueprint('historial', __name__, url_prefix='/historial')

@historial_bp.route('/')
def historial():
    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    conn = sqlite3.connect('bitacoras.db')
    cursor = conn.cursor()

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


@historial_bp.route('/exportar')
def exportar_bitacoras():
    conn = sqlite3.connect('bitacoras.db')
    df = pd.read_sql_query("SELECT * FROM registros ORDER BY id DESC", conn)
    conn.close()

    file_path = os.path.join('static', 'historial_completo.xlsx')
    df.to_excel(file_path, index=False)

    return send_file(file_path, as_attachment=True)
