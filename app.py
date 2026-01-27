


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
                height:100vh;
                display:flex;
                justify-content:center;
                align-items:center;
                background:linear-gradient(180deg,#071a2d,#0b2a44);
                font-family:Arial;
                color:white;
            }}
            .box {{
                background:#061627;
                padding:40px;
                border-radius:14px;
                width:320px;
                text-align:center;
            }}
            h1 {{
                font-weight:bold;
            }}
            .x {{
                color:#e74c3c;
            }}
            input,button {{
                width:100%;
                padding:12px;
                margin-top:15px;
            }}
            button {{
                background:#4da6ff;
                border:none;
                color:white;
                cursor:pointer;
            }}
            .error {{
                color:#ff7675;
                margin-top:10px;
            }}
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
        body {
            margin:0;
            font-family:Arial;
            background:linear-gradient(180deg,#071a2d,#0b2a44);
            color:white;
        }

        .nav {
            background:#061627;
            padding:15px 40px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        }

        .brand {
            font-weight:bold;
        }

        .brand .x {
            color:#e74c3c;
        }

        .content {
            padding:40px;
        }

        h1 {
            margin-bottom:10px;
        }

        .kpis {
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
            gap:20px;
            margin-bottom:40px;
        }

        .box {
            background:#102a43;
            padding:20px;
            border-radius:14px;
            text-align:center;
        }

        .layout {
            display:grid;
            grid-template-columns: 1fr 1.2fr;
            gap:30px;
            margin-top:40px;
        }

        .chart-box {
            background:#102a43;
            padding:20px;
            border-radius:14px;
            height:320px;
        }

        .chart-box canvas {
            max-height:260px;
        }

        .map-box {
            background:#102a43;
            padding:20px;
            border-radius:14px;
        }

        #map {
            height:320px;
            border-radius:10px;
            margin-top:10px;
        }

        select {
            padding:10px;
            width:100%;
            margin-top:10px;
        }
    </style>
</head>

<body>

    <div class="nav">
        <div>RUTOGRAMA OPERATIVO</div>
        <div class="brand">SODE<span class="x">X</span>O PERÚ</div>
    </div>

    <div class="content">
        <h1>🗺️ Rutograma de Atención</h1>

        <div class="kpis">
            <div class="box"><h2>6</h2>Vehículos</div>
            <div class="box"><h2>5</h2>Técnicos</div>
            <div class="box"><h2>5</h2>Oficinas</div>
            <div class="box"><h2>42</h2>Tickets Pendientes</div>
        </div>

        <div class="layout">
            <!-- BARRAS -->
            <div class="chart-box">
                <h3>Tickets por Oficina</h3>
                <canvas id="barChart"></canvas>
            </div>

            <!-- MAPA -->
            <div class="map-box">
                <h3>Rutas por Técnico</h3>
                <select id="tecnico" onchange="cambiarRuta()">
                    <option value="1">Técnico Juan</option>
                    <option value="2">Técnico Carlos</option>
                    <option value="3">Técnico Luis</option>
                    <option value="4">Técnico Pedro</option>
                    <option value="5">Técnico Ana</option>
                </select>
                <div id="map"></div>
            </div>
        </div>
    </div>

<script>
    // Gráfico de barras
    new Chart(document.getElementById('barChart'), {
        type:'bar',
        data:{
            labels:['San Isidro','Surco','Miraflores','Callao','Chorrillos'],
            datasets:[{
                data:[12,9,7,8,6],
                backgroundColor:'#4da6ff'
            }]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false,
            plugins:{ legend:{display:false} }
        }
    });

    // MAPA
    var map = L.map('map').setView([-12.0464,-77.0428],14);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom:19
    }).addTo(map);

    var rutas = {
        1: [[-12.045,-77.04],[-12.047,-77.035],[-12.05,-77.03]],
        2: [[-12.05,-77.045],[-12.052,-77.05],[-12.055,-77.055]],
        3: [[-12.04,-77.03],[-12.042,-77.028],[-12.044,-77.026]],
        4: [[-12.048,-77.06],[-12.049,-77.065],[-12.05,-77.07]],
        5: [[-12.043,-77.05],[-12.041,-77.048],[-12.039,-77.046]]
    };

    var polyline = L.polyline(rutas[1],{color:'red', weight:4}).addTo(map);

    function cambiarRuta(){
        map.removeLayer(polyline);
        var t = document.getElementById('tecnico').value;
        polyline = L.polyline(rutas[t],{color:'red', weight:4}).addTo(map);
        map.fitBounds(polyline.getBounds());
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
