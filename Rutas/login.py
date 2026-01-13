from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from flask import send_file
import sqlite3, os
import pandas as pd

app = Flask(__name__)
app.secret_key = "admin123"

@app.route('/')
def index():
    if "usuario" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        password = request.form['password']

        conn = sqlite3.connect('bitacoras.db')
        c = conn.cursor()
        c.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (usuario, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['usuario'] = user[1]  # Guarda el nombre del usuario
            session['rol'] = user[3]      # Guarda el rol (OMT o Administrador)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Usuario o contraseña incorrectos")

    return render_template('login.html')
