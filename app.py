from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secreto_prueba"

USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDA = "Prueba123"


# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form.get("usuario") == USUARIO_VALIDO and request.form.get("password") == PASSWORD_VALIDA:
            session["logueado"] = True
            return redirect(url_for("principal"))
        else:
            error = "Usuario o contraseña incorrectos"

    return f"""
    <html>
    <head>
        <title>Login | Sodexo Perú</title>
        <style>
            body {{
                height:100vh; display:flex; justify-content:center; align-items:center;
                background:linear-gradient(180deg,#071a2d,#0b2a44);
                font-family:Arial; color:white;
            }}
            .box {{
                background:#061627; padding:40px; border-radius:14px;
                width:320px; text-align:center;
            }}
            .x {{ color:#e74c3c; }}
            input,button {{ width:100%; padding:12px; margin-top:15px; }}
            button {{ background:#4da6ff; border:none; color:white; }}
            .error {{ color:#ff7675; margin-top:10px; }}
        </style>
    </head>
    <body>
        <form method="POST" class="box">
            <h1>SODE<span class="x">X</span>O PERÚ</h1>
            <h3>Acceso Rutograma</h3>
            <input name="usuario" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button>Ingresar</button>
            <div class="error">{error}</div>
        </form>
    </body>
    </html>
    """


# =========================
# LAYOUT BASE
# =========================
def layout(titulo, contenido):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{titulo} | Sodexo Perú</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <style>
        body {{
            margin:0; font-family:Arial;
            background:linear-gradient(180deg,#071a2d,#0b2a44);
            color:white;
        }}

        .nav {{
            background:#061627;
            padding:15px 40px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }}

        .brand .x {{ color:#e74c3c; font-weight:bold; }}

        .subnav {{
            background:#0b2238;
            padding:10px 40px;
            display:flex;
            gap:25px;
        }}

        .subnav a {{
            color:#cce6ff;
            text-decoration:none;
            font-weight:bold;
        }}

        .subnav a:hover {{ color:#4da6ff; }}

        .content {{ padding:40px; }}

        .logout {{
            color:#ff7675;
            text-decoration:none;
            font-weight:bold;
        }}

        .box {{
            background:#102a43;
            padding:20px;
            border-radius:14px;
            margin-bottom:20px;
        }}

        .grid {{
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
            gap:20px;
        }}

        #map {{ height:320px; border-radius:10px; }}
    </style>
</head>

<body>

<div class="nav">
    <div class="brand">SODE<span class="x">X</span>O PERÚ</div>
    <a class="logout" href="/logout">Cerrar sesión</a>
</div>

<div class="subnav">
    <a href="/principal">Principal</a>
    <a href="/tecnicos">Técnicos</a>
    <a href="/especialidad">Especialidad</a>
    <a href="/clientes">Clientes</a>
    <a href="/condiciones">Condiciones</a>
</div>

<div class="content">
    <h1>{titulo}</h1>
    {contenido}
</div>

</body>
</html>
"""


# =========================
# PRINCIPAL (RUTOGRAMA)
# =========================
@app.route("/principal")
def principal():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="grid">
        <div class="box"><h2>6</h2>Vehículos</div>
        <div class="box"><h2>5</h2>Técnicos</div>
        <div class="box"><h2>5</h2>Oficinas</div>
        <div class="box"><h2>42</h2>Tickets</div>
    </div>

    <div class="box">
        <h3>Rutas Operativas</h3>
        <select onchange="cambiarRuta(this.value)">
            <option value="1">Técnico Juan</option>
            <option value="2">Técnico Carlos</option>
            <option value="3">Técnico Ana</option>
            <option value="4">Técnico Luis</option>
            <option value="5">Técnico Pedro</option>
        </select>
        <div id="map"></div>
    </div>

    <script>
        var map = L.map('map').setView([-12.0464,-77.0428],14);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

        var rutas = {
            1:[[-12.045,-77.04],[-12.047,-77.035],[-12.05,-77.03]],
            2:[[-12.05,-77.045],[-12.052,-77.05]],
            3:[[-12.04,-77.03],[-12.042,-77.028]],
            4:[[-12.048,-77.06],[-12.049,-77.065]],
            5:[[-12.043,-77.05],[-12.041,-77.048]]
        };

        var linea = L.polyline(rutas[1],{color:'red'}).addTo(map);

        function cambiarRuta(v){
            map.removeLayer(linea);
            linea = L.polyline(rutas[v],{color:'red'}).addTo(map);
            map.fitBounds(linea.getBounds());
        }
    </script>
    """
    return layout("Principal – Rutograma", contenido)


# =========================
# TÉCNICOS
# =========================
@app.route("/tecnicos")
def tecnicos():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="grid">
        <div class="box">Juan – Zona Centro</div>
        <div class="box">Carlos – Zona Norte</div>
        <div class="box">Ana – Zona Sur</div>
        <div class="box">Luis – Callao</div>
        <div class="box">Pedro – Soporte</div>
    </div>
    """
    return layout("Técnicos", contenido)


# =========================
# ESPECIALIDAD
# =========================
@app.route("/especialidad")
def especialidad():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="grid">
        <div class="box">Electricidad – 40%</div>
        <div class="box">Climatización – 25%</div>
        <div class="box">Gas – 20%</div>
        <div class="box">Otros – 15%</div>
    </div>
    """
    return layout("Especialidades", contenido)


# =========================
# CLIENTES
# =========================
@app.route("/clientes")
def clientes():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="grid">
        <div class="box">Cliente A – 12 tickets</div>
        <div class="box">Cliente B – 9 tickets</div>
        <div class="box">Cliente C – 7 tickets</div>
    </div>
    """
    return layout("Clientes", contenido)


# =========================
# CONDICIONES
# =========================
@app.route("/condiciones")
def condiciones():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="box">
        <p>Las rutas se asignan según disponibilidad, SLA y prioridad contractual.
        Este rutograma es de uso interno y referencial.</p>
    </div>
    """
    return layout("Condiciones Operativas", contenido)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

