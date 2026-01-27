
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
    <head>
      <style>
        body {
          margin:0;
          height:100vh;
          background:linear-gradient(180deg,#071a2f,#0b2a4a);
          display:flex;
          align-items:center;
          justify-content:center;
          font-family:Arial;
        }
        .login-box {
          background:#081c34;
          padding:35px;
          border-radius:16px;
          width:340px;
          text-align:center;
          box-shadow:0 20px 40px rgba(0,0,0,.4);
        }
        h1 { margin:0;color:white;letter-spacing:1px; }
        .x { color:red; }
        h3 { margin-top:10px;color:#9fbad6;font-weight:normal; }
        input {
          width:100%;
          padding:12px;
          margin-top:15px;
          border-radius:8px;
          border:none;
        }
        button {
          width:100%;
          margin-top:20px;
          padding:12px;
          background:#4da3ff;
          border:none;
          color:white;
          border-radius:8px;
          font-size:15px;
          cursor:pointer;
        }
      </style>
    </head>
    <body>
      <div class="login-box">
        <h1>SODE<span class="x">X</span>O PERÚ</h1>
        <h3>Acceso Rutograma</h3>
        <form method="post">
          <input name="usuario" placeholder="Usuario">
          <input type="password" name="password" placeholder="Contraseña">
          <button>Ingresar</button>
        </form>
      </div>
    </body>
    </html>
    """

# =========================
# MAPAS
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
        .menu {{
          background:#0b2a4a;
          padding:10px 20px;
          display:flex;
          gap:14px;
          font-size:14px;
        }}
        .menu a {{ color:white;text-decoration:none }}
        .separator {{ color:#4da3ff }}
        .content {{ padding:20px }}
        .card {{ background:#102a43;padding:20px;border-radius:12px }}
        .kpi {{
          display:flex;
          align-items:center;
          gap:10px;
          font-size:15px;
        }}
        .kpi-number {{
          margin-top:8px;
          font-size:26px;
          font-weight:bold;
        }}
      </style>
    </head>
    <body>

      <div class="top">
        <b>SODE<span style="color:red">X</span>O PERÚ</b>
        <a href="/logout" style="float:right;color:red">Cerrar sesión</a>
      </div>

      <div class="menu">
        <a href="/principal">Principal</a><span class="separator">|</span>
        <a href="/tecnicos">Técnicos</a><span class="separator">|</span>
        <a href="/especialidad">Especialidad</a><span class="separator">|</span>
        <a href="/clientes">Clientes</a><span class="separator">|</span>
        <a href="/condiciones">Condiciones</a>
      </div>

      <div class="content">
        {contenido}
      </div>

    </body>
    </html>
    """

# =========================
# PRINCIPAL
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
      <div class="card" style="flex:1">
        <div class="kpi">🚚 <b>Vehículos</b></div>
        <div class="kpi-number">6</div>
      </div>
      <div class="card" style="flex:1;background:#244a4a">
        <div class="kpi">🧑‍🔧 <b>Técnicos</b></div>
        <div class="kpi-number">5</div>
      </div>
      <div class="card" style="flex:1;background:#2c9c8c">
        <div class="kpi">🏢 <b>Oficinas</b></div>
        <div class="kpi-number">5</div>
      </div>
      <div class="card" style="flex:1;background:#e67352">
        <div class="kpi">🎫 <b>Tickets</b></div>
        <div class="kpi-number">42</div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <div class="card" style="height:450px">
        <h3 style="margin-top:0">Tickets por oficina</h3>
        <canvas id="barras" style="height:100%"></canvas>
      </div>

      <div class="card" style="height:450px">
        <select onchange="location='?tecnico='+this.value"
        style="
          width:100%;
          height:42px;
          font-size:16px;
          padding:6px 10px;
          border-radius:8px;
          margin-bottom:12px;
        ">






        
          {''.join([f"<option {'selected' if t==tecnico else ''}>{t}</option>" for t in RUTAS])}
        </select>
        <iframe src="{mapa}" style="width:100%;height:100%;border:0;border-radius:10px"></iframe>
      </div>
    </div>

    <script>
    new Chart(document.getElementById('barras'), {{
      type:'bar',
      data:{{
        labels:['San Isidro','Surco','Miraflores','Callao','Chorrillos'],
        datasets:[{{data:[12,9,7,8,6],backgroundColor:'#4da3ff'}}]
      }},
      options:{{
        maintainAspectRatio:false,
        plugins:{{legend:{{display:false}}}},
        scales:{{
          x:{{ticks:{{color:'white'}}}},
          y:{{ticks:{{color:'white'}}}}
        }}
      }}
    }});
    </script>
    """

    return layout("Rutograma", contenido)

# =========================
# OTRAS PÁGINAS
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

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)






