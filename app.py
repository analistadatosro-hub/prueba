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

        <!-- Chart.js -->
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2"></script>

        <style>
            body {
                margin: 0;
                font-family: 'Segoe UI', Arial, sans-serif;
                background: #0b1c2d;
                color: #ffffff;
            }

            header {
                background: #081522;
                padding: 16px 40px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }

            .menu a {
                color: #cfd8e3;
                margin-right: 25px;
                text-decoration: none;
                font-weight: 500;
            }

            .brand {
                font-weight: bold;
                color: #4da3ff;
            }

            main {
                padding: 40px;
            }

            h1 {
                margin-bottom: 10px;
            }

            .subtitle {
                color: #9fb3c8;
                margin-bottom: 40px;
            }

            .kpis {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
                gap: 25px;
                margin-bottom: 50px;
            }

            .card {
                background: linear-gradient(135deg, #102a43, #243b53);
                padding: 25px;
                border-radius: 14px;
                text-align: center;
            }

            .card h2 {
                font-size: 36px;
                margin: 0;
            }

            .card p {
                color: #cbd5e1;
            }

            .charts {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 40px;
            }

            canvas {
                background: #102a43;
                padding: 20px;
                border-radius: 14px;
            }

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

        <header>
            <div class="menu">
                <a href="#">Inicio</a>
                <a href="#">Responsable</a>
                <a href="#">Contratos</a>
            </div>
            <div class="brand">SODEXO PERÚ</div>
        </header>

        <main>
            <h1>📊 Dashboard de Atención de Tickets</h1>
            <div class="subtitle">
                Seguimiento operativo – datos simulados
            </div>

            <!-- KPIs -->
            <div class="kpis">
                <div class="card"><h2 style="color:#4da3ff">150</h2><p>Total Tickets</p></div>
                <div class="card"><h2 style="color:#2ecc71">98</h2><p>A Tiempo</p></div>
                <div class="card"><h2 style="color:#f1c40f">32</h2><p>Fuera de Tiempo</p></div>
                <div class="card"><h2 style="color:#e74c3c">20</h2><p>Pendientes</p></div>
            </div>

            <!-- Charts -->
            <div class="charts">
                <canvas id="barChart"></canvas>
                <canvas id="pieChart"></canvas>
            </div>
        </main>

        <footer>
            Dashboard de Control • Sodexo Perú • Uso interno
        </footer>

        <script>
            Chart.register(ChartDataLabels);

            // Gráfico de barras - Distritos
            new Chart(document.getElementById('barChart'), {
                type: 'bar',
                data: {
                    labels: ['San Isidro', 'Miraflores', 'Surco', 'Callao', 'Arequipa'],
                    datasets: [{
                        label: 'Tickets por Distrito',
                        data: [40, 32, 28, 20, 30],
                        backgroundColor: '#4da3ff'
                    }]
                },
                options: {
                    plugins: {
                        datalabels: {
                            color: '#fff',
                            anchor: 'end',
                            align: 'top'
                        },
                        legend: { display: false }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: { color: '#cbd5e1' }
                        },
                        x: {
                            ticks: { color: '#cbd5e1' }
                        }
                    }
                }
            });

            // Gráfico pastel - Lima vs Provincia
            new Chart(document.getElementById('pieChart'), {
                type: 'pie',
                data: {
                    labels: ['Lima', 'Provincia'],
                    datasets: [{
                        data: [110, 40],
                        backgroundColor: ['#2ecc71', '#f39c12']
                    }]
                },
                options: {
                    plugins: {
                        datalabels: {
                            color: '#fff',
                            formatter: (value, ctx) => {
                                let total = ctx.chart.data.datasets[0].data.reduce((a,b)=>a+b,0);
                                return Math.round((value / total) * 100) + '%';
                            }
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

