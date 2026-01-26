from flask import Flask

app = Flask(__name__)

@app.route("/")
def dashboard():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Dashboard Tickets | Sodexo Perú</title>
        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #0b1c2d;
                color: #ffffff;
            }

            /* ===== HEADER ===== */
            header {
                background: #081522;
                padding: 16px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.4);
            }

            .menu a {
                color: #cfd8e3;
                margin-right: 25px;
                text-decoration: none;
                font-weight: 500;
            }

            .menu a:hover {
                color: #4da3ff;
            }

            .brand {
                font-weight: bold;
                letter-spacing: 1px;
                color: #4da3ff;
            }

            /* ===== MAIN ===== */
            main {
                padding: 40px;
            }

            h1 {
                margin-bottom: 10px;
                font-size: 28px;
            }

            .subtitle {
                color: #9fb3c8;
                margin-bottom: 40px;
            }

            /* ===== KPI CARDS ===== */
            .container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 25px;
            }

            .card {
                background: linear-gradient(135deg, #102a43, #243b53);
                padding: 25px;
                border-radius: 14px;
                box-shadow: 0 6px 18px rgba(0,0,0,0.35);
                text-align: center;
                transition: transform 0.2s ease;
            }

            .card:hover {
                transform: translateY(-5px);
            }

            .card h2 {
                font-size: 38px;
                margin: 0;
            }

            .card p {
                margin-top: 8px;
                color: #cbd5e1;
                font-size: 15px;
                letter-spacing: 0.5px;
            }

            .kpi-total h2 { color: #4da3ff; }
            .kpi-ok h2 { color: #2ecc71; }
            .kpi-alert h2 { color: #f1c40f; }
            .kpi-pending h2 { color: #e74c3c; }

            /* ===== FOOTER ===== */
            footer {
                margin-top: 60px;
                padding: 20px;
                text-align: center;
                font-size: 13px;
                color: #9fb3c8;
                border-top: 1px solid #1f3a56;
            }
        </style>
    </head>

    <body>

        <!-- HEADER -->
        <header>
            <div class="menu">
                <a href="#">Inicio</a>
                <a href="#">Responsable</a>
                <a href="#">Contratos</a>
            </div>
            <div class="brand">SODEXO PERÚ</div>
        </header>

        <!-- MAIN CONTENT -->
        <main>
            <h1>📊 Dashboard de Atención de Tickets</h1>
            <div class="subtitle">
                Seguimiento operativo – datos simulados (prueba de concepto)
            </div>

            <div class="container">
                <div class="card kpi-total">
                    <h2>150</h2>
                    <p>Total de Tickets</p>
                </div>

                <div class="card kpi-ok">
                    <h2>98</h2>
                    <p>Atendidos a Tiempo</p>
                </div>

                <div class="card kpi-alert">
                    <h2>32</h2>
                    <p>Fuera de Tiempo</p>
                </div>

                <div class="card kpi-pending">
                    <h2>20</h2>
                    <p>Pendientes</p>
                </div>
            </div>
        </main>

        <!-- FOOTER -->
        <footer>
            Dashboard de Control • Sodexo Perú • Uso interno
        </footer>

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

