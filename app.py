from flask import Flask

app = Flask(__name__)

@app.route("/")
def dashboard():
    return """
    <html>
    <head>
        <title>Dashboard Tickets - Prueba</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f2f2f2;
                padding: 40px;
            }
            .container {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
            }
            .card {
                background: white;
                padding: 20px;
                width: 200px;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            }
            h1 {
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <h1>📊 Dashboard de Atención de Tickets (PRUEBA)</h1>

        <div class="container">
            <div class="card">
                <h2>150</h2>
                <p>Total Tickets</p>
            </div>

            <div class="card">
                <h2>98</h2>
                <p>Atendidos a Tiempo</p>
            </div>

            <div class="card">
                <h2>32</h2>
                <p>Fuera de Tiempo</p>
            </div>

            <div class="card">
                <h2>20</h2>
                <p>Pendientes</p>
            </div>
        </div>

        <p style="margin-top:40px;color:gray;">
            Datos simulados – prueba de concepto
        </p>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
