from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secret_key"

# =========================
# CREDENCIALES (PRUEBA)
# =========================
USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDO = "Prueba123"

# =========================
# RUTAS GOOGLE MAPS (EMBED)
# =========================
RUTAS_TECNICOS = {
    "Juan": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764063242456!2d-77.010256!3d-12.088906!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1s0x9105c87bda9e6db7%3A0x8c7b8c7e6a4d4f32!2sSan%20Isidro%2C%20Lima!3m2!1d-12.097955!2d-77.037018!4m5!1s0x9105c84ff2d0fbe9%3A0x5d2a6a5e2f5c41fa!2sMiraflores%2C%20Lima!3m2!1d-12.1215!2d-77.0297!5e0!3m2!1ses!2spe!4v1700000000001",
    "Pedro": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764063242456!2d-77.030346!3d-12.091313!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1sSurco%2C%20Lima!3m2!1d-12.1337!2d-77.0211!4m5!1sChorrillos%2C%20Lima!3m2!1d-12.1702!2d-77.0243!5e0!3m2!1ses!2spe!4v1700000000002",
    "Luis": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764063242456!2d-77.042!3d-12.055!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1sCallao!3m2!1d-12.0621!2d-77.1335!4m5!1sLa%20Punta!3m2!1d-12.0741!2d-77.1654!5e0!3m2!1ses!2spe!4v1700000000003",
    "Carlos": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764063242456!2d-77.012!3d-12.099!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1sSan%20Borja!3m2!1d-12.107!2d-77.001!4m5!1sLa%20Victoria!3m2!1d-12.066!2d-77.033!5e0!3m2!1ses!2spe!4v1700000000004",
    "Miguel": "https://www.google.com/maps/embed?pb=!1m28!1m12!1m3!1d3901.8764063242456!2d-77.060!3d-12.090!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!4m13!3e0!4m5!1sMagdalena!3m2!1d-12.089!2d-77.070!4m5!1sPueblo%20Libre!3m2!1d-12.078!2d-77.062!5e0!3m2!1ses!2spe!4v1700000000005",
}

# =========================
# LOGIN
# =========================
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
    <html><body style="background:#081c34;color:white;font-family:Arial;text-align:center;padding-top:120px">
    <h1>SODEXO <span style="color:red">X</span> PERÚ</h1>
    <form method="post">
      <input name="usuario" placeholder="Usuario"><br><br>
      <input type="password" name="password" placeholder="Contraseña"><br><br>
      <button>Ingresar</button>
    </form>
    </body></html>
    """

# =========================
# PRINCIPAL - RUTOGRAMA
# =========================
@app.route("/principal")
def principal():
    if not session.get("login"):
        return redirect(url_for("login"))

    tecnico = request.args.get("tecnico", "Juan")
    mapa = RUTAS_TECNICOS.get(tecnico)

    return f"""
    <html>
    <head>
      <title>Rutograma - Sodexo Perú</title>
      <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
      <style>
        body {{ background:#071a2f;color:white;font-family:Arial;margin:0 }}
        .top {{ padding:15px;background:#081c34 }}
        .menu {{ display:flex;gap:20px;padding:10px 20px;background:#0b2a4a }}
        .menu a {{ color:white;text-decoration:none }}
        .cards {{ display:flex;gap:20px;padding:20px }}
        .card {{ flex:1;padding:20px;border-radius:12px;text-align:center }}
        .c1{{background:#1e3a5f}} .c2{{background:#244a4a}}
        .c3{{background:#2c9c8c}} .c4{{background:#e67352}}
        .grid {{ display:flex;gap:20px;padding:20px }}
        iframe {{ border-radius:12px }}
      </style>
    </head>
    <body>

    <div class="top">
      <b>SODEXO <span style="color:red">X</span> PERÚ</b>
      <a href="/logout" style="float:right;color:red">Cerrar sesión</a>
    </div>

    <div class="menu">
      <a href="/principal">Principal</a>
      <a href="#">Técnicos</a>
      <a href="#">Especialidad</a>
      <a href="#">Clientes</a>
      <a href="#">Condiciones</a>
    </div>

    <h2 style="padding:20px">Principal – Rutograma</h2>

    <div class="cards">
      <div class="card c1">🚚<h2>6</h2>Vehículos</div>
      <div class="card c2">🧑‍🔧<h2>5</h2>Técnicos</div>
      <div class="card c3">🏢<h2>5</h2>Oficinas</div>
      <div class="card c4">🎫<h2>42</h2>Tickets</div>
    </div>

    <div class="grid">
      <canvas id="bar" width="400"></canvas>

      <div>
        <select onchange="location='?tecnico='+this.value">
          {''.join([f"<option {'selected' if t==tecnico else ''}>{t}</option>" for t in RUTAS_TECNICOS])}
        </select><br><br>

        <iframe src="{mapa}" width="500" height="350"></iframe>
      </div>
    </div>

    <script>
    new Chart(document.getElementById('bar'), {{
      type:'bar',
      data:{{
        labels:['San Isidro','Surco','Miraflores','Callao','Chorrillos'],
        datasets:[{{data:[12,9,7,8,6],backgroundColor:'#4da3ff'}}]
      }},
      options:{{plugins:{{legend:{{display:false}}}}}}
    }});
    </script>

    </body>
    </html>
    """

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
