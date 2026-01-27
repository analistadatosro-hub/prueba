from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secreto_prueba"

USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDA = "Prueba123"


# ================= LOGIN =================
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


# ================= LAYOUT BASE =================
def layout(titulo, contenido, extra_js=""):
    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>{titulo}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {{
            margin:0; font-family:Arial;
            background:linear-gradient(180deg,#071a2d,#0b2a44);
            color:white;
        }}
        .nav {{
            background:#061627;
            padding:15px 40px;
            display:flex; justify-content:space-between; align-items:center;
        }}
        .brand .x {{ color:#e74c3c; }}
        .subnav {{
            background:#0b2238; padding:10px 40px;
            display:flex; gap:25px;
        }}
        .subnav a {{
            color:#cce6ff; text-decoration:none; font-weight:bold;
        }}
        .subnav a:hover {{ color:#4da6ff; }}
        .logout {{ color:#ff7675; text-decoration:none; font-weight:bold; }}
        .content {{ padding:40px; }}
        .grid {{
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(200px,1fr));
            gap:20px;
        }}
        .card {{
            background:#102a43;
            padding:20px;
            border-radius:14px;
            text-align:center;
        }}
        .row {{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:30px;
            margin-top:30px;
        }}
        iframe {{
            border-radius:10px;
        }}
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

{extra_js}
</body>
</html>
"""


# ================= PRINCIPAL =================
@app.route("/principal")
def principal():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    contenido = """
    <div class="grid">
        <div class="card" style="background:#1f3a56;">🚚<h2>6</h2>Vehículos</div>
        <div class="card" style="background:#264653;">👷<h2>5</h2>Técnicos</div>
        <div class="card" style="background:#2a9d8f;">🏢<h2>5</h2>Oficinas</div>
        <div class="card" style="background:#e76f51;">🎫<h2>42</h2>Tickets</div>
    </div>

    <div class="row">
        <!-- GRAFICO -->
        <div class="card">
            <h3>Tickets por Oficina</h3>
            <canvas id="barChart"></canvas>
        </div>

        <!-- MAPA GOOGLE -->
        <div class="card">
            <h3>Ruta por Técnico</h3>
            <select onchange="cambiarRuta(this.value)">
                <option value="1">Técnico Juan</option>
                <option value="2">Técnico Carlos</option>
                <option value="3">Técnico Ana</option>
                <option value="4">Técnico Luis</option>
                <option value="5">Técnico Pedro</option>
            </select>

            <iframe
                id="mapa"
                width="100%"
                height="300"
                src=""
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade">
            </iframe>
        </div>
    </div>
    """

    extra_js = """
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
            options:{ plugins:{legend:{display:false}} }
        });

        // RUTAS GOOGLE MAPS (UNA POR TECNICO)
        const rutas = {
            1: "https://www.google.com/maps/dir/?api=1&waypoints=-12.088906,-77.004256&destination=-12.091313,-77.030346&travelmode=driving",
            2: "https://www.google.com/maps/dir/?api=1&waypoints=-12.060000,-77.045000&destination=-12.070000,-77.060000&travelmode=driving",
            3: "https://www.google.com/maps/dir/?api=1&waypoints=-12.050000,-77.030000&destination=-12.040000,-77.020000&travelmode=driving",
            4: "https://www.google.com/maps/dir/?api=1&waypoints=-12.080000,-77.070000&destination=-12.090000,-77.080000&travelmode=driving",
            5: "https://www.google.com/maps/dir/?api=1&waypoints=-12.100000,-77.040000&destination=-12.110000,-77.050000&travelmode=driving"
        };

        function cambiarRuta(v){
            document.getElementById("mapa").src = rutas[v];
        }

        // Ruta inicial
        cambiarRuta(1);
    </script>
    """

    return layout("Principal – Rutograma", contenido, extra_js)


# ================= OTRAS PÁGINAS (NO TOCADAS) =================
@app.route("/tecnicos")
def tecnicos():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return layout("Técnicos", "<div class='card'>Vista de técnicos</div>")

@app.route("/especialidad")
def especialidad():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return layout("Especialidad", "<div class='card'>Vista de especialidades</div>")

@app.route("/clientes")
def clientes():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return layout("Clientes", "<div class='card'>Vista de clientes</div>")

@app.route("/condiciones")
def condiciones():
    if not session.get("logueado"):
        return redirect(url_for("login"))
    return layout("Condiciones", "<div class='card'>Condiciones operativas</div>")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)


