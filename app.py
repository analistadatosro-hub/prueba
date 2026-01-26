from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "sodexo_secreto_prueba"

# Credenciales de prueba
USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDA = "Prueba123"


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        usuario = request.form.get("usuario")
        password = request.form.get("password")

        if usuario == USUARIO_VALIDO and password == PASSWORD_VALIDA:
            session["logueado"] = True
            return redirect(url_for("dashboard"))
        else:
            error = "Usuario o contraseña incorrectos"

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Login | Sodexo Perú</title>
        <style>
            body {{
                margin: 0;
                height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                font-family: Arial, sans-serif;
                background: linear-gradient(180deg, #071a2d, #0b2a44);
                color: white;
            }}

            .login-box {{
                background: #061627;
                padding: 40px;
                border-radius: 14px;
                width: 320px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4);
                text-align: center;
            }}

            h1 {{
                margin-bottom: 5px;
                color: #4da6ff;
            }}

            h3 {{
                margin-top: 0;
                margin-bottom: 30px;
                font-weight: normal;
                color: #cce6ff;
            }}

            input {{
                width: 100%;
                padding: 12px;
                margin-bottom: 15px;
                border-radius: 6px;
                border: none;
                font-size: 14px;
            }}

            button {{
                width: 100%;
                padding: 12px;
                background: #4da6ff;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                cursor: pointer;
            }}

            button:hover {{
                background: #2e8cff;
            }}

            .error {{
                margin-top: 15px;
                color: #ff7675;
                font-size: 13px;
            }}
        </style>
    </head>
    <body>
        <form method="POST" class="login-box">
            <h1>SODEXO PERÚ</h1>
            <h3>Acceso a Dashboard</h3>

            <input type="text" name="usuario" placeholder="Usuario" required>
            <input type="password" name="password" placeholder="Contraseña" required>

            <button type="submit">Ingresar</button>

            <div class="error">{error}</div>
        </form>
    </body>
    </html>
    """


@app.route("/dashboard")
def dashboard():
    if not session.get("logueado"):
        return redirect(url_for("login"))

    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Tickets | Sodexo Perú</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(180deg, #071a2d, #0b2a44);
                color: #ffffff;
            }

            .navbar {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 40px;
                background: #061627;
            }

            .navbar a {
                color: #cce6ff;
                margin-right: 20px;
                text-decoration: none;
                font-weight: bold;
            }

            .brand {
                color: #4da6ff;
                font-weight: bold;
            }

            .content {
                padding: 40px;
            }

            .kpis {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }

            .kpi {
                background: #102a43;
                border-radius: 14px;
                padding: 25px;
                text-align: center;
            }

            .charts {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
                gap: 30px;
            }

            .chart-box {
                background: #102a43;
                border-radius: 14px;
                padding: 20px;
                height: 380px;
            }

            .chart-box canvas {
                max-height: 300px !important;
            }
        </style>
    </head>

    <body>
        <div class="navbar">
            <div>
                <a href="#">Inicio</a>
                <a href="#">Responsable</a>
                <a href="#">Contratos</a>
            </div>
            <div class="brand">SODEXO PERÚ</div>
        </div>

        <div class="content">
            <h1>📊 Dashboard de Atención de Tickets</h1>

            <div class="kpis">
                <div class="kpi"><h2 style="color:#4da6ff">150</h2>Total</div>
                <div class="kpi"><h2 style="color:#2ecc71">98</h2>A Tiempo</div>
                <div class="kpi"><h2 style="color:#f1c40f">32</h2>Fuera de Tiempo</div>
                <div class="kpi"><h2 style="color:#e74c3c">20</h2>Pendientes</div>
            </div>

            <div class="charts">
                <div class="chart-box">
                    <canvas id="barChart"></canvas>
                </div>
                <div class="chart-box">
                    <canvas id="pieChart"></canvas>
                </div>
            </div>
        </div>

        <script>
            new Chart(document.getElementById('barChart'), {
                type: 'bar',
                data: {
                    labels: ['San Isidro', 'Miraflores', 'Surco', 'Callao', 'Chiclayo'],
                    datasets: [{
                        data: [40, 32, 28, 22, 18],
                        backgroundColor: '#4da6ff'
                    }]
                }
            });

            new Chart(document.getElementById('pieChart'), {
                type: 'pie',
                data: {
                    labels: ['Lima', 'Provincia'],
                    datasets: [{
                        data: [65, 35],
                        backgroundColor: ['#2ecc71', '#f39c12']
                    }]
                }
            });
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


