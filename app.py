import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from vrp_solver import solve_vrp_data, format_solution, generate_folium_map
import io
import os
import math
import shutil

# =========================
# CONFIG STREAMLIT
# =========================
st.set_page_config(page_title="Gestión de Rutas - Sodexo", layout="wide", page_icon="🚛")

# =========================
# LOGIN CONFIG
# =========================
USUARIO_VALIDO = "ABEDOYA"
PASSWORD_VALIDA = "Prueba123"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        st.markdown("""
        <div style="
            background:#081c34;
            padding:40px;
            border-radius:16px;
            text-align:center;
            box-shadow:0 20px 40px rgba(0,0,0,.35);
        ">
            <h1 style="color:white;margin-bottom:5px">
                SODE<span style="color:#EF4044">X</span>O PERÚ
            </h1>
            <p style="color:#c7d3e3;margin-top:0">
                Acceso Rutograma
            </p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            usuario = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            ingresar = st.form_submit_button("Ingresar")

            if ingresar:
                if usuario == USUARIO_VALIDO and password == PASSWORD_VALIDA:
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos")


# =========================
# LOGIN CHECK
# =========================
if not st.session_state.logged_in:
    login_page()
    st.stop()

# =========================
# CUSTOM CSS (SODEXO BRANDING) - SOLO DESPUÉS DEL LOGIN
# =========================
st.markdown(
    """
    <style>
    /* Main Background */
    .stApp {
        background-color: #F4F6F8;
    }

    /* Headers - Sodexo Navy */
    h1, h2, h3, h4, h5, h6 {
        color: #262262 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Buttons - Sodexo Red */
    .stButton button {
        background-color: #EF4044 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        transition: all 0.3s ease !important;
    }
    .stButton button:hover {
        background-color: #D12F33 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
    }

    /* Metrics Styles */
    div[data-testid="stMetricValue"] {
        color: #EF4044 !important;
        font-weight: bold;
    }
    div[data-testid="stMetricLabel"] {
        color: #5D5D5D !important;
    }

    /* Cards/Containers */
    div[data-testid="stExpander"] {
        border-color: #E0E0E0 !important;
        border-radius: 8px !important;
        background-color: white !important;
    }

    /* Tables */
    thead tr th:first-child {display:none}
    tbody th {display:none}

    /* INPUTS & MENUS - Gray Background, Blue Text */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div, .stTextArea textarea {
        background-color: #E0E4E8 !important;
        color: #262262 !important;
        border-radius: 5px;
        border: 1px solid #B0B0B0 !important;
    }

    /* Dropdown Menu Container */
    div[data-baseweb="popover"], div[data-baseweb="popover"] > div, ul[data-baseweb="menu"] {
        background-color: #E0E4E8 !important;
    }

    /* Dropdown Options Text */
    li[data-baseweb="option"] span, li[data-baseweb="option"] div, .stSelectbox [data-baseweb="menu"] li {
        color: #262262 !important;
    }

    /* Selected Option Background (Hover) */
    li[data-baseweb="option"]:hover, li[data-baseweb="option"][aria-selected="true"] {
        background-color: #CCD3D9 !important;
    }

    /* Selected Text in Input Box */
    div[data-baseweb="select"] span {
        color: #262262 !important;
    }

    /* Remove white/dark default backgrounds on the list container */
    .stSelectbox ul {
        background-color: #E0E4E8 !important;
    }

    /* HEADERS - FORCE BLUE */
    h1, h2, h3, h4, h5, h6,
    .stHeadingContainer h1, .stHeadingContainer h2, .stHeadingContainer h3,
    div[data-testid="stMarkdownContainer"] h1, div[data-testid="stMarkdownContainer"] h2, div[data-testid="stMarkdownContainer"] h3,
    div[data-testid="stMarkdownContainer"] p,
    .stMarkdown label p {
        color: #262262 !important;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Ensure widgets label texts are also blue */
    .stSelectbox label, .stTextInput label, .stNumberInput label {
        color: #262262 !important;
    }

    /* Metric Labels */
    div[data-testid="stMetricLabel"] {
        color: #262262 !important;
    }

    /* DATAFRAMES / TABLES - Force Gray Background */
    [data-testid="stDataFrame"], [data-testid="stTable"] {
        background-color: #E0E4E8 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


st.markdown("""
<style>

/* 🔥 QUITAR ESPACIO SUPERIOR GLOBAL */
.main .block-container {
    padding-top: 0.5rem !important;
    padding-bottom: 1rem !important;
}

/* 🔥 PEGAR LOGO Y TITULO ARRIBA */
h1, h2, h3 {
    margin-top: 0 !important;
    padding-top: 0 !important;
}

/* 🔥 REDUCIR ESPACIO DESPUÉS DEL LOGO */
img {
    margin-bottom: 0.5rem !important;
}

/* 🔥 QUITAR ESPACIO EXTRA DE STREAMLIT */
section[data-testid="stSidebar"] + div {
    padding-top: 0 !important;
}

</style>
""", unsafe_allow_html=True)




# =========================
# SESSION STATE INITIALIZATION
# =========================
if "stage" not in st.session_state:
    st.session_state.stage = "input_tickets"  # input_tickets, fleet_config, results
if "daily_tickets" not in st.session_state:
    st.session_state.daily_tickets = []
if "master_db" not in st.session_state:
    st.session_state.master_db = None
if "optimization_result" not in st.session_state:
    st.session_state.optimization_result = None


# =========================
# HELPERS
# =========================
def style_dataframe(df):
    return df.style.set_properties(
        **{
            "background-color": "#E0E4E8",
            "color": "#262262",
            "border-color": "#FFFFFF",
        }
    ).set_table_styles(
        [
            {
                "selector": "th",
                "props": [
                    ("background-color", "#CCD3D9"),
                    ("color", "#262262"),
                    ("font-weight", "bold"),
                ],
            }
        ]
    )


def reset_app():
    st.session_state.stage = "input_tickets"
    st.session_state.daily_tickets = []
    st.session_state.optimization_result = None


# =========================
# APP HEADER
# =========================
# APP HEADER - LOGO
if os.path.exists("logo.jpeg"):
    st.image("logo.jpeg", width=220)
else:
    st.markdown("<h1 style='text-align: center; color: #262262; padding-top: 0px;'>Planificador de Rutas</h1>", unsafe_allow_html=True)



st.markdown(
    "<h1 style='text-align: center; color: #262262; padding-top: 10px;'>Planificador de Rutas</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: #5D5D5D; font-weight: bold;'>Gestión Inteligente de Flota y Entregas - Sodexo Perú</p>",
    unsafe_allow_html=True,
)

if st.button("🔄 Reiniciar Aplicación"):
    reset_app()
    st.rerun()


# =========================
# LOAD DATABASE (ONLY VIA UPLOAD)
# =========================
if st.session_state.master_db is None:
    uploaded = st.file_uploader(
        "📂 Sube el archivo maestro Excel (VRP_Spreadsheet_Solver_v3.8 14.05.xlsm)",
        type=["xlsx", "xlsm"],
    )

    if uploaded is None:
        st.info("⬆️ Por favor sube el archivo Excel para continuar.")
        st.stop()

    try:
        df_db = pd.read_excel(uploaded, sheet_name="1 ubicaciones")
        df_db.columns = df_db.columns.str.strip()

        for col in ["Latitud (y)", "Longitud (x)"]:
            if col in df_db.columns:
                df_db[col] = pd.to_numeric(df_db[col], errors="coerce")

        st.session_state.master_db = df_db
        st.success("✅ Base de Datos cargada correctamente.")
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error al leer el archivo Excel: {e}")
        st.stop()


# =========================
# STAGE 1: INGRESO DE TICKETS
# =========================
if st.session_state.stage == "input_tickets":
    st.header("1️⃣ Ingreso de Tickets del Día")

    col_input, col_table = st.columns([1, 2])

    with col_input:
        tab_manual, tab_import = st.tabs(["📝 Manual", "📂 Importar Excel"])

        with tab_manual:
            st.subheader("Nuevo Ticket Individual")

            if "Habla a" in st.session_state.master_db.columns:
                clients = sorted(st.session_state.master_db["Habla a"].astype(str).unique().tolist())
                selected_client = st.selectbox("Filtrar por Cliente", options=["Todos"] + clients)
            else:
                selected_client = st.selectbox("Filtrar por Cliente", options=["Todos"], disabled=True)

            if selected_client != "Todos":
                filtered_db = st.session_state.master_db[
                    st.session_state.master_db["Habla a"].astype(str) == selected_client
                ]
                office_options = filtered_db["Nombre"].unique().tolist()
            else:
                office_options = st.session_state.master_db["Nombre"].unique().tolist()

            with st.form("ticket_form", clear_on_submit=True):
                selected_office = st.selectbox("Seleccionar Oficina", options=sorted(office_options))
                ticket_id = st.text_input("Nro Ticket (ID)")
                familia = st.text_input("Familia / Especialidad")

                add_btn = st.form_submit_button("➕ Agregar a la Lista")

                if add_btn:
                    if not ticket_id:
                        st.warning("Por favor ingrese un número de ticket.")
                    else:
                        office_data = st.session_state.master_db[
                            st.session_state.master_db["Nombre"] == selected_office
                        ].iloc[0]

                        st.session_state.daily_tickets.append(
                            {
                                "Nombre": selected_office,
                                "Habla a": office_data.get("Habla a", ""),
                                "Ticket": ticket_id,
                                "Familia": familia,
                                "Latitud (y)": office_data["Latitud (y)"],
                                "Longitud (x)": office_data["Longitud (x)"],
                                "Importe de la entrega": 1,
                            }
                        )
                        st.toast(f"Ticket {ticket_id} agregado!", icon="👍")

        with tab_import:
            st.subheader("Carga Masiva")
            uploaded_tickets = st.file_uploader(
                "Subir Excel (Columnas: Oficina, Ticket, Familia)",
                type=["xlsx", "xls", "csv"],
            )

            if uploaded_tickets:
                try:
                    if uploaded_tickets.name.endswith(".csv"):
                        df_upload = pd.read_csv(uploaded_tickets)
                    else:
                        df_upload = pd.read_excel(uploaded_tickets)

                    st.write("Vista Previa:", df_upload.head(3))

                    if st.button("Procesar Archivo"):
                        col_oficina = next(
                            (c for c in df_upload.columns if "oficina" in c.lower() or "nombre" in c.lower()),
                            None,
                        )
                        col_ticket = next(
                            (c for c in df_upload.columns if "ticket" in c.lower() or "numero" in c.lower()),
                            None,
                        )
                        col_familia = next((c for c in df_upload.columns if "familia" in c.lower()), None)

                        if not col_oficina:
                            st.error("No se encontró columna para 'Oficina' o 'Nombre'.")
                        else:
                            success_count = 0
                            fail_count = 0

                            for _, row in df_upload.iterrows():
                                office_name = row[col_oficina]
                                match = st.session_state.master_db[st.session_state.master_db["Nombre"] == office_name]

                                if not match.empty:
                                    office_data = match.iloc[0]
                                    st.session_state.daily_tickets.append(
                                        {
                                            "Nombre": office_name,
                                            "Habla a": office_data.get("Habla a", ""),
                                            "Ticket": row[col_ticket] if col_ticket else "N/A",
                                            "Familia": row[col_familia] if col_familia else "General",
                                            "Latitud (y)": office_data["Latitud (y)"],
                                            "Longitud (x)": office_data["Longitud (x)"],
                                            "Importe de la entrega": 1,
                                        }
                                    )
                                    success_count += 1
                                else:
                                    fail_count += 1

                            st.success(f"Procesado: {success_count} tickets agregados.")
                            if fail_count > 0:
                                st.warning(f"{fail_count} oficinas no encontradas en la Base Maestra.")

                except Exception as e:
                    st.error(f"Error procesando: {e}")

    with col_table:
        st.subheader("📋 Lista de Pendientes")
        if st.session_state.daily_tickets:
            df_display = pd.DataFrame(st.session_state.daily_tickets)
            st.dataframe(
                style_dataframe(df_display[["Nombre", "Ticket", "Familia"]]),
                use_container_width=True,
            )

            if st.button("✅ Confirmar y Configurar Flota", type="primary"):
                st.session_state.stage = "fleet_config"
                st.rerun()
        else:
            st.info("Agregue tickets para continuar.")


# =========================
# STAGE 2: CONFIGURACION DE FLOTA
# =========================
elif st.session_state.stage == "fleet_config":
    st.header("2️⃣ Disponibilidad de Vehículos")

    col_config, col_summary = st.columns(2)

    with col_config:
        st.info("Ingrese los recursos disponibles para hoy:")

        num_vehicles = st.number_input("Cantidad de Camionetas Disponibles", min_value=1, value=5)
        max_capacity = st.number_input("Capacidad Max (Tickets por camioneta)", min_value=1, value=100)

        col_adv_1, col_adv_2 = st.columns(2)
        service_time = col_adv_1.number_input(
            "Tiempo de Servicio por Ticket (min)",
            min_value=1,
            value=15,
            help="Tiempo estimado para entregar 1 ticket",
        )
        max_work_hours = col_adv_2.number_input(
            "Jornada Maxima (horas)",
            min_value=4,
            value=12,
            help="Duración máxima de ruta por camioneta",
        )

        trafico = st.selectbox("Condición de Tráfico", ["Normal", "Pesado", "Ligero"])
        tf_factor = 1.0
        if trafico == "Pesado":
            tf_factor = 1.6
        if trafico == "Ligero":
            tf_factor = 0.8

        col_act_1, col_act_2 = st.columns(2)
        if col_act_1.button("🔙 Volver"):
            st.session_state.stage = "input_tickets"
            st.rerun()

        if col_act_2.button("🚀 Calcular Rutas", type="primary"):
            df_raw = pd.DataFrame(st.session_state.daily_tickets)

            df_grouped = (
                df_raw.groupby(["Nombre", "Latitud (y)", "Longitud (x)", "Habla a"])
                .agg(
                    {
                        "Importe de la entrega": "sum",
                        "Ticket": lambda x: ", ".join(x.astype(str)),
                        "Familia": lambda x: ", ".join(x.unique()),
                    }
                )
                .reset_index()
            )

            with st.spinner("Optimizando rutas..."):
                solution, routing, manager, data, df_cleaned = solve_vrp_data(
                    df_grouped,
                    num_vehicles,
                    max_capacity,
                    traffic_factor=tf_factor,
                    service_time_per_ticket_mins=service_time,
                    max_work_hours=max_work_hours,
                )

                if solution:
                    st.session_state.optimization_result = (solution, routing, manager, data, df_cleaned)
                    st.session_state.stage = "results"
                    st.rerun()
                else:
                    st.error("❌ No se encontró solución con los recursos actuales.")

                    total_tickets = df_grouped["Importe de la entrega"].sum()
                    total_service_mins = total_tickets * service_time
                    num_offices = len(df_grouped)
                    est_travel_mins = num_offices * 30 * tf_factor
                    total_work_load_mins = total_service_mins + est_travel_mins

                    max_single_tickets = df_grouped["Importe de la entrega"].max()
                    max_single_time_mins = max_single_tickets * service_time
                    problematic_office = df_grouped.loc[df_grouped["Importe de la entrega"].idxmax()]["Nombre"]

                    work_day_mins = max_work_hours * 60

                    if max_single_time_mins > work_day_mins:
                        st.error(
                            f"""
                        🛑 **Imposible de procesar:**
                        La oficina **"{problematic_office}"** tiene **{max_single_tickets} tickets**, lo que requiere **{int(max_single_time_mins/60)} horas** de servicio.
                        Esto excede la jornada máxima de {max_work_hours} horas.

                        **Solución:** Reduzca el "Tiempo de Servicio" o aumente la "Jornada Maxima".
                        """
                        )
                    else:
                        min_veh_cap = math.ceil(total_tickets / max_capacity)
                        min_veh_time = math.ceil(total_work_load_mins / work_day_mins)
                        suggested_min = max(int(min_veh_cap), int(min_veh_time))

                        width_veh_time = total_work_load_mins / num_vehicles
                        avg_status = "✅" if width_veh_time <= work_day_mins else "❌"
                        avg_msg = "" if width_veh_time <= work_day_mins else "*(El promedio supera la jornada máxima)*"

                        st.warning(
                            f"""
                        **Diagnóstico del Fallo:**
                        El sistema no encontró solución.

                        **Análisis de Tiempo (Estimado):**
                        - Carga Total (Servicio + Viaje): **{int(total_work_load_mins/60)} horas**
                        - Max por Camioneta: **{max_work_hours} horas**
                        - Promedio actual ({num_vehicles} veh): **{int(width_veh_time/60)} horas** {avg_status} {avg_msg}

                        **Sugerencia:**
                        Se sugieren al menos **{suggested_min} camionetas**.
                        Si ya tiene {suggested_min}, el problema puede ser la dispersión geográfica. Intente aumentar ligeramente la jornada (+1h).
                        """
                        )

    with col_summary:
        st.write(f"**Total Tickets:** {len(st.session_state.daily_tickets)}")
        st.write("**Oficinas a visitar:**")
        df_display = pd.DataFrame(st.session_state.daily_tickets)
        office_counts = df_display.groupby("Nombre").size().reset_index(name="Tickets")
        st.dataframe(office_counts, use_container_width=True, hide_index=True)


# =========================
# STAGE 3: RESULTADOS
# =========================
elif st.session_state.stage == "results":
    st.header("3️⃣ Rutas Optimizadas")

    solution, routing, manager, data, df_loc = st.session_state.optimization_result
    results, route_maps_data, total_duration, total_load = format_solution(
        data, manager, routing, solution, df_loc
    )

    c1, c2, c3 = st.columns(3)
    num_active_routes = len([r for r in route_maps_data if r["load"] > 0])

    if num_active_routes > 0:
        avg_duration = total_duration / num_active_routes
        hours = int(avg_duration / 3600)
        mins = int((avg_duration % 3600) / 60)
    else:
        hours, mins = 0, 0

    c1.metric("Tiempo Promedio por Ruta", f"{hours}h {mins}m")
    c2.metric("Tickets Atendidos", total_load)
    c3.metric("Camionetas Utilizadas", num_active_routes)

    st.subheader("🗺️ Visualización de Rutas")
    m_result = generate_folium_map(df_loc, route_maps_data)
    st_folium(m_result, height=500, width="100%")

    st.subheader("📝 Detalle de Visitas (Consolidado)")
    df_res = pd.DataFrame(results).sort_values(by=["VehicleID", "OrderInRoute"])
    st.dataframe(
        style_dataframe(df_res[["VehicleID", "OrderInRoute", "LocationName", "Client", "AccumulatedDuration_Mins"]]),
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("🚚 Itinerarios por Camioneta")

    unique_vehicles = df_res["VehicleID"].unique()

    for vid in unique_vehicles:
        vehicle_route = df_res[df_res["VehicleID"] == vid]
        with st.expander(f"Camioneta #{vid + 1} ({len(vehicle_route)} paradas)", expanded=True):
            st.write(f"**Tiempo Estimado:** {vehicle_route['AccumulatedDuration_Mins'].max()} min")

            path_steps = []
            maps_waypoints = []

            for _, row in vehicle_route.iterrows():
                loc_str = row["LocationName"]
                if row["Client"]:
                    loc_str += f" ({row['Client']})"
                path_steps.append(loc_str)

                if (
                    "Latitude" in row
                    and "Longitude" in row
                    and pd.notnull(row["Latitude"])
                    and pd.notnull(row["Longitude"])
                ):
                    maps_waypoints.append(f"{row['Latitude']},{row['Longitude']}")

            flow_str = " ➝ ".join(path_steps)
            st.info(f"**Secuencia de Visita:**\n\n🏁 Inicio ➝ {flow_str} ➝ 🏁 Fin")

            if maps_waypoints:
                waypoints_str = "/".join(maps_waypoints)
                maps_url = f"https://www.google.com/maps/dir/{waypoints_str}"
                st.link_button("🗺️ Abrir Ruta en Google Maps", maps_url)

            for _, stop in vehicle_route.iterrows():
                client_str = f" ({stop['Client']})" if stop["Client"] else ""
                st.markdown(f"**{stop['OrderInRoute']}. {stop['LocationName']}{client_str}**")

    # Export Excel (requiere openpyxl instalado)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_res.to_excel(writer, index=False, sheet_name="Hoja de Ruta")

    c_down, c_reset = st.columns([1, 4])
    c_down.download_button(
        "📥 Descargar Excel",
        buffer.getvalue(),
        "rutas_sodexo.xlsx",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    if c_reset.button("🔄 Nueva Planificación"):
        reset_app()
        st.rerun()





