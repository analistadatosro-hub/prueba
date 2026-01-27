from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secreto_prueba"

USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDA = "Prueba123"


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        if request.form.get("usuario") == USUARIO_VALIDO and request.form.get("password") == PASSWORD_VALIDA:
            session["logueado"] = True
            return redirect(url_for("rutograma"))
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
            h1 {{ color:#e74c3c; }}
            input,button {{ width:100%; padding:12px; margin-top:15px; }}
            button {{ background:#4da6ff; border:none; color:white; }}
            .error {{ color:#ff7675; margin-top:10px; }}
        </style>
    </head>
    <body>
        <form method="POST" class="box">
            <h1>SODEXO ✖</h1>
            <h3>Acceso Rutograma</h3>
            <input name="usuario" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>
            <button>Ingresar</button>
            <div class="error">{error}</div>
        </form>
    </body>
    </html>
    """


@app.route("/rutograma")
def rutograma():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    return """
<!DOCTYPE html>
<html>
<head>
    <title>Rutograma | Sodexo Perú</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

    <style>
        body { margin:0; font-family:Arial; background:linear-gradient(180deg,#071a2d,#0b2a44); color:white; }
        .nav { background:#061627; padding:15px 40px; display:flex; justify-content:space-between; }
        .brand { color:#e74c3c; font-weight:bold; }
        .content { padding:40px; }
        .kpis, .charts { display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:20px; }
        .box { background:#102a43; padding:20px; border-radius:14px; text-align:center; }
        #map { height:400px; border-radius:14px; margin-top:30px; }
        select { padding:10px; margin-bottom:20px; }
    </style>
</head>

<body>
    <div class="nav">
        <div>Rutograma Operativo</div>
        <div class="brand">SODEXO ✖ PERÚ</div>
    </div>

    <div class="content">
        <h1>🗺️ Rutograma de Atención</h1>

        <div class="kpis">
            <div class="box"><h2>6</h2>Vehículos</div>
            <div class="box"><h2>8</h2>Técnicos</div>
            <div class="box"><h2>5</h2>Oficinas</div>
            <div class="box"><h2>42</h2>Tickets Pendientes</div>
        </div>

        <h3 style="margin-top:40px;">📊 Tickets por Oficina</h3>
        <div class="charts">
            <div class="box"><canvas id="barChart"></canvas></div>
        </div>

        <h3 style="margin-top:40px;">👷 Filtro por Técnico</h3>
        <select id="tecnico" onchange="cambiarRuta()">
            <option value="1">Técnico Juan</option>
            <option value="2">Técnico Carlos</option>
        </select>

        <div id="map"></div>
    </div>

<script>
    new Chart(document.getElementById('barChart'), {
        type:'bar',
        data:{
            labels:['San Isidro','Surco','Miraflores','Callao','Chorrillos'],
            datasets:[{data:[12,9,7,8,6], backgroundColor:'#4da6ff'}]
        }
    });

    var map = L.map('map').setView([-12.0464,-77.0428],12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

    var rutas = {
        1: [[-12.05,-77.04],[-12.06,-77.03],[-12.07,-77.02]],
        2: [[-12.04,-77.05],[-12.03,-77.06],[-12.02,-77.07]]
    };

    var polyline = L.polyline(rutas[1],{color:'red'}).addTo(map);

    function cambiarRuta(){
        map.removeLayer(polyline);
        var t = document.getElementById('tecnico').value;
        polyline = L.polyline(rutas[t],{color:'red'}).addTo(map);
    }
</script>
</body>
</html>
"""


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

