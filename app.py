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
# RUTAS GOOGLE MAPS
# =========================
RUTAS = {
    "Juan": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764!2d-77.004256!3d-12.088906!4m13!3e0!4m5!1sSan+Isidro!4m5!1sMiraflores!5e0",
    "Pedro": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764!2d-77.0211!3d-12.1337!4m13!3e0!4m5!1sSurco!4m5!1sChorrillos!5e0",
    "Luis": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764!2d-77.1335!3d-12.0621!4m13!3e0!4m5!1sCallao!4m5!1sLa+Punta!5e0",
    "Carlos": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764!2d-77.001!3d-12.107!4m13!3e0!4m5!1sSan+Borja!4m5!1sLa+Victoria!5e0",
    "Miguel": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764!2d-77.070!3d-12.089!4m13!3e0!4m5!1sMagdalena!4m5!1sPueblo+Libre!5e0",
}

# =========================
# LAYOUT BASE (NO TOCAR)
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
# PRINCIPAL (ÚNICO AJUSTE)
# =========================
@app.route("/principal")
def principal():
    if not session.get("login"):
        return redirect(url_for("login"))

    tecnico = request.args.get("tecnico", "Juan")
    mapa = RUTAS.get(tecnico)

    contenido = f"""
    <h2>Principal – Rutograma</h2>

    <div style="display:flex;gap:20px;margin-bottom:20px">
      <div style="flex:1;background:#1e3a5f;padding:20px;border-radius:12px;text-align:center">🚚<h2>6</h2>Vehículos</div>
      <div style="flex:1;background:#244a4a;padding:20px;border-radius:12px;text-align:center">🧑‍🔧<h2>5</h2>Técnicos</div>
      <div style="flex:1;background:#2c9c8c;padding:20px;border-radius:12px;text-align:center">🏢<h2>5</h2>Oficinas</div>
      <div style="flex:1;background:#e67352;padding:20px;border-radius:12px;text-align:center">🎫<h2>42</h2>Tickets</div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <canvas id="barras"></canvas>
      <div>
        <select onchange="location='?tecnico='+this.value">
          {''.join([f"<option {'selected' if t==tecnico else ''}>{t}</option>" for t in RUTAS])}
        </select><br><br>
        <iframe src="{mapa}" width="100%" height="350" style="border-radius:12px;border:none"></iframe>
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
# OTRAS PÁGINAS (SIN TOCAR)
# =========================
@app.route("/tecnicos")
def tecnicos():
    return layout("Técnicos", "<h2>Técnicos</h2><p>Contenido existente</p>")

@app.route("/especialidad")
def especialidad():
    return layout("Especialidad", "<h2>Especialidad</h2><p>Contenido existente</p>")

@app.route("/clientes")
def clientes():
    return layout("Clientes", "<h2>Clientes</h2><p>Contenido existente</p>")

@app.route("/condiciones")
def condiciones():
    return layout("Condiciones", "<h2>Condiciones</h2><p>Contenido existente</p>")

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
