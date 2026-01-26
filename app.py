from flask import Flask

app = Flask(__name__)

@app.route("/")
def dashboard():
    return """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Dashboard Tickets - Sodexo Perú</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(180deg, #071a2d, #0b2a44);
            color: #ffffff;
        }

        /* Barra superior */
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

        .navbar a:hover {
            color: #4da6ff;
        }

        .brand {
            color: #4da6ff;
            font-weight: bold;
            font-size: 16px;
        }

        /* Contenido */
        .content {
            padding: 40px;
        }

        h1 {
            margin-bottom: 5px;
        }

        .subtitle {
            color: #b0cde6;
            margin-bottom: 30px;
        }

        /* KPIs */
        .kpis {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .kpi {
            background: linear-gradient(180deg, #102a43, #0b2238);
            border-radius: 14px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        }

        .kpi h2 {
            font-size: 38px;
            margin: 0;
        }

        .kpi p {
            margin-top: 10px;
            color: #cce6ff;
        }

        .blue { color: #4da6ff; }
        .green { color: #2ecc71; }
        .yellow { color: #f1c40f; }
        .red { color: #e74c3c; }

        /* Gráficos */
        .charts {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 30px;
        }

        .chart-box {
            background: linear-gradient(180deg, #102a43, #0b2238);
            border-radius: 14px;
            padding: 20px;
            height: 380px;
        }

        .chart-box canvas {
            max-height: 300px !important;
        }

        footer {
            margin-top: 40px;
            text-align: center;
            font-size: 12px;
            color: #9bbbd4;
        }
    </style>
</head>

<body>

    <!-- NAVBAR -->
    <div class="navbar">
        <div>
            <a href="#">Inicio</a>
            <a href="#">Responsable</a>
            <a href="#">Contratos</a>
        </div>
        <div class="brand">SODEXO PERÚ</div>
    </div>

    <!-- CONTENIDO -->
    <div class="content">
        <h1>📊 Dashboard de Atención de Tickets</h1>
        <div class="subtitle">
            Seguimiento operativo – datos simulados (prueba de concepto)
        </div>

        <!-- KPIs -->
        <div class="kpis">
            <div class="kpi">
                <h2 class="blue">150</h2>
                <p>Total Tickets</p>
            </div>
            <div class="kpi">
                <h2 class="green">98</h2>
                <p>A Tiempo</p>
            </div>
            <div class="kpi">
                <h2 class="yellow">32</h2>
                <p>Fuera de Tiempo</p>
            </div>
            <div class="kpi">
                <h2 class="red">20</h2>
                <p>Pendientes</p>
            </div>
        </div>

        <!-- GRAFICOS -->
        <div class="charts">
            <div class="chart-box">
                <canvas id="barChart"></canvas>
            </div>

            <div class="chart-box">
                <canvas id="pieChart"></canvas>
            </div>
        </div>

        <footer>
            Dashboard de Control · Sodexo Perú · Uso interno
        </footer>
    </div>

    <!-- CHART JS -->
    <script>
        // Barras - Distritos
        new Chart(document.getElementById('barChart'), {
            type: 'bar',
            data: {
                labels: ['San Isidro', 'Miraflores', 'Surco', 'Callao', 'Chiclayo'],
                datasets: [{
                    label: 'Tickets por Agencia',
                    data: [40, 32, 28, 22, 18],
                    backgroundColor: '#4da6ff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        ticks: { color: '#cce6ff' },
                        grid: { color: '#1f3b57' }
                    },
                    x: {
                        ticks: { color: '#cce6ff' },
                        grid: { display: false }
                    }
                }
            }
        });

        // Pastel - Lima vs Provincia
        new Chart(document.getElementById('pieChart'), {
            type: 'pie',
            data: {
                labels: ['Lima', 'Provincia'],
                datasets: [{
                    data: [65, 35],
                    backgroundColor: ['#2ecc71', '#f39c12']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#cce6ff' }
                    }
                }
            }
        });
    </script>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
