from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secret_key"

# =========================
# LOGIN (NO TOCAR)
# =========================
USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDO = "Prueba123"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if (
            request.form["usuario"] == USUARIO_VALIDO
            and request.form["password"] == PASSWORD_VALIDO
        ):
            session["login"] = True
            return redirect(url_for("principal"))
    return """
    <html>
    <body style="background:#081c34;color:white;font-family:Arial;text-align:center;padding-top:120px">
      <h1>SODEXO <span style="color:red">X</span> PERÚ</h1>
      <form method="post">
        <input name="usuario" placeholder="Usuario"><br><br>
        <input type="password" name="password" placeholder="Contraseña"><br><br>
        <button>Ingresar</button>
      </form>
    </body>
    </html>
    """

# =========================
# MAPAS GOOGLE (EMBED VÁLIDO)
# =========================
RUTAS = {
    "Juan": "https://www.google.com/maps?q=San+Isidro+Lima&output=embed",
    "Pedro": "https://www.google.com/maps?q=Surco+Lima&output=embed",
    "Luis": "https://www.google.com/maps?q=Callao+Lima&output=embed",
    "Carlos": "https://www.google.com/maps?q=San+Borja+Lima&output=embed",
    "Miguel": "https://www.google.com/maps?q=Magdalena+Lima&output=embed",
}

# =========================
# LAYOUT BASE
# =========================
def layout(titulo, contenido):
    return f"""
    <html>
    <head>
      <title>{titulo}</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        body {{ margin:0;background:#071a2f;color:white;font-family:Arial }}
        .top {{ background:#081c34;padding:15px }}
        .menu {{ background:#0b2a4a;padding:10px 20px;display:flex;gap:20px }}
        .menu a {{ color:white;text-decoration:none }}
        .content {{ padding:20px }}
        .card {{ background:#102a43;padding:20px;border-radius:12px;margin-bottom:15px }}
      </style>
    </head>
    <body>

      <div class="top">
        <b>SODEXO <span style="color:red">X</span> PERÚ</b>
        <a href="/logout" style="float:right;color:red">Cerrar sesión</a>
      </div>

      <div class="menu">
        <a href="/principal">Principal</a>
        <a href="/tecnicos">Técnicos</a>
        <a href="/especialidad">Especialidad</a>
        <a href="/clientes">Clientes</a>
        <a href="/condiciones">Condiciones</a>
      </div>

      <div class="content">
        {contenido}
      </div>

    </body>
    </html>
    """

# =========================
# PRINCIPAL (SOLO MAPA ARREGLADO)
# =========================
@app.route("/principal")
def principal():
    if not session.get("login"):
        return redirect(url_for("login"))

    tecnico = request.args.get("tecnico", "Juan")
    mapa = RUTAS.get(tecnico)

    contenido = f"""
    <h2>Principal – Rutograma</h2>

    <div style="display:flex;gap:20px;margin-bottom:25px">
      <div style="flex:1;background:#1e3a5f;padding:20px;border-radius:12px;text-align:center">🚚<h2>6</h2>Vehículos</div>
      <div style="flex:1;background:#244a4a;padding:20px;border-radius:12px;text-align:center">🧑‍🔧<h2>5</h2>Técnicos</div>
      <div style="flex:1;background:#2c9c8c;padding:20px;border-radius:12px;text-align:center">🏢<h2>5</h2>Oficinas</div>
      <div style="flex:1;background:#e67352;padding:20px;border-radius:12px;text-align:center">🎫<h2>42</h2>Tickets</div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">

      <div class="card">
        <canvas id="barras" height="180"></canvas>
      </div>

      <div class="card">
        <select onchange="location='?tecnico='+this.value" style="width:100%;margin-bottom:10px">
          {''.join([f"<option {'selected' if t==tecnico else ''}>{t}</option>" for t in RUTAS])}
        </select>

        <iframe src="{mapa}" width="100%" height="180" style="border:0;border-radius:10px"></iframe>
      </div>

    </div>

    <script>
    new Chart(document.getElementById('barras'), {{
      type:'bar',
      data:{{
        labels:['San Isidro','Surco','Miraflores','Callao','Chorrillos'],
        datasets:[{{data:[12,9,7,8,6],backgroundColor:'#4da3ff'}}]
      }},
      options:{{plugins:{{legend:{{display:false}}}}}}
    }});
    </script>
    """

    return layout("Rutograma", contenido)

# =========================
# RESTO DE PÁGINAS (CONTENIDO CREATIVO)
# =========================
@app.route("/tecnicos")
def tecnicos():
    return layout("Técnicos", """
    <h2>Técnicos Asignados</h2>
    <div class="card">🧑‍🔧 Juan – Electricidad</div>
    <div class="card">🧑‍🔧 Pedro – Climatización</div>
    <div class="card">🧑‍🔧 Luis – Infraestructura</div>
    <div class="card">🧑‍🔧 Carlos – Redes</div>
    <div class="card">🧑‍🔧 Miguel – Seguridad</div>
    """)

@app.route("/especialidad")
def especialidad():
    return layout("Especialidad", """
    <h2>Especialidades Técnicas</h2>
    <div class="card">⚡ Electricidad Industrial</div>
    <div class="card">❄️ Climatización y HVAC</div>
    <div class="card">🛠️ Mantenimiento General</div>
    <div class="card">🌐 Redes y Comunicaciones</div>
    """)

@app.route("/clientes")
def clientes():
    return layout("Clientes", """
    <h2>Clientes Atendidos</h2>
    <div class="card">🏦 BCP</div>
    <div class="card">🏦 BBVA</div>
    <div class="card">🏦 Interbank</div>
    <div class="card">🏦 Scotiabank</div>
    """)

@app.route("/condiciones")
def condiciones():
    return layout("Condiciones", """
    <h2>Condiciones de Atención</h2>
    <div class="card">⏱️ SLA estándar: 24 horas</div>
    <div class="card">🚨 Atención crítica: 4 horas</div>
    <div class="card">📍 Cobertura Lima y provincias</div>
    <div class="card">📑 Registro obligatorio de cierre</div>
    """)

# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# =========================
# RUN
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
