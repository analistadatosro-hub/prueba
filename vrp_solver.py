
import pandas as pd
import numpy as np
import math
import folium
import os
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from datetime import datetime

# --- CONFIGURATION ---
INPUT_FILE = "VRP_Spreadsheet_Solver_v3.8 14.05.xlsm"

OUTPUT_MAP = "mapa_rutas_peru.html"
OUTPUT_EXCEL = "solucion_rutas.xlsx"

def haversine(lat1, lon1, lat2, lon2):
    """Calculates the great circle distance in km between two points."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def create_duration_matrix(locations, traffic_factor=1.0):
    """
    Creates a duration matrix (seconds) from locations.
    Traffic factor > 1.0 means slower traffic (longer duration).
    Base Speed assumption: 40 km/h in city.
    """
    print(f"Calculating duration matrix with Traffic Factor: {traffic_factor}")
    n = len(locations)
    
    # Base speed in km/h
    # If traffic_factor is 1.0 (Normal), speed is 30 km/h
    # If traffic_factor is 1.5 (High Traffic), speed is 20 km/h
    base_speed_kmh = 30 / traffic_factor 
    base_speed_ms = base_speed_kmh * (1000 / 3600)
    
    coords = locations[['Latitud (y)', 'Longitud (x)']].values
    
    full_matrix = []
    for from_node in range(n):
        row = []
        for to_node in range(n):
            if from_node == to_node:
                row.append(0)
            else:
                dist_km = haversine(coords[from_node][0], coords[from_node][1], 
                                  coords[to_node][0], coords[to_node][1])
                dist_m = int(dist_km * 1000)
                
                # Duration in seconds = Distance (m) / Speed (m/s)
                # Add a base penalty for stopping/turning (e.g. 5 minutes fixed per trip?) 
                # For pure travel time:
                duration_s = int(dist_m / base_speed_ms)
                row.append(duration_s)
        full_matrix.append(row)
        
    return full_matrix

def solve_vrp_data(df_loc, num_vehicles, vehicle_capacity, start_node_index=0, max_seconds=30, traffic_factor=1.0, 
                   service_time_per_ticket_mins=15, max_work_hours=12):
    """
    Solves VRP for given dataframe of locations and vehicle parameters.
    Optimizes for TIME (Duration).
    Returns: (solution object, routing model, manager, data_dict) or None
    """
    num_locations = len(df_loc)
    print(f"Solving for {num_locations} locations with {num_vehicles} vehicles (Cap: {vehicle_capacity})")

    # CLEANING: Ensure coordinates are numeric
    for col in ['Latitud (y)', 'Longitud (x)']:
        if col in df_loc.columns:
            df_loc[col] = pd.to_numeric(df_loc[col], errors='coerce')
            
    # Remove NaN coordinates just in case
    df_loc = df_loc.dropna(subset=['Latitud (y)', 'Longitud (x)'])
    num_locations = len(df_loc) # Re-calculate after drop

    # Build Vehicle Config
    vehicle_capacities = [vehicle_capacity] * num_vehicles
    starts = [start_node_index] * num_vehicles
    ends = [start_node_index] * num_vehicles
    
    # SETUP DATA MODEL
    data = {}
    
    # COST MATRIX is now DURATION (seconds)
    data['time_matrix'] = create_duration_matrix(df_loc, traffic_factor)
    
    # Demands
    if 'Importe de la entrega' in df_loc.columns:
        demands = df_loc['Importe de la entrega'].fillna(0).astype(int).tolist()
    elif 'Tickets' in df_loc.columns:
        demands = df_loc['Tickets'].fillna(0).astype(int).tolist()
    else:
        demands = [0] * num_locations 
        
    data['demands'] = demands
    data['vehicle_capacities'] = vehicle_capacities
    data['num_vehicles'] = num_vehicles
    data['starts'] = starts
    data['ends'] = ends
    
    # OR-TOOLS SETUP
    # Use time_matrix size
    manager = pywrapcp.RoutingIndexManager(len(data['time_matrix']),
                                           data['num_vehicles'],
                                           data['starts'],
                                           data['ends'])
    
    routing = pywrapcp.RoutingModel(manager)
    
    # Time/Duration Callback
    service_time_seconds = service_time_per_ticket_mins * 60
    
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        # Add service time per ticket
        service_time = data['demands'][from_node] * service_time_seconds 
        travel_time = data['time_matrix'][from_node][to_node]
        return travel_time + service_time

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
    
    # Capacity Constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')
    
    # Add Time Dimension
    max_time_seconds = max_work_hours * 3600
    routing.AddDimension(
        transit_callback_index,
        max_time_seconds, # Allow waiting time? (Max slack)
        max_time_seconds, # Max route duration
        False, # Don't start to zero (accumulate)
        'Time')
    
    # Add Global Span Cost to balance routes
    time_dimension = routing.GetDimensionOrDie('Time')
    time_dimension.SetGlobalSpanCostCoefficient(100)

    # SOLVE
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.seconds = max_seconds
    
    solution = routing.SolveWithParameters(search_parameters)
    return solution, routing, manager, data, df_loc

def format_solution(data, manager, routing, solution, df_loc):
    """Formats solution into standard structure for display/export"""
    total_duration = 0
    total_load = 0
    
    results = [] 
    route_maps_data = [] # For plotting

    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        route_duration = 0
        route_load = 0
        route_nodes = []
        route_coords = []
        
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            
            # Cost is roughly seconds now
            duration = routing.GetArcCostForVehicle(previous_index, index, vehicle_id)
            route_duration += duration
            
            # Data collection
            # Skip the start node (Depot) in the Excel report to avoid "repeating offices"
            # and to avoid listing vehicles that don't leave the depot.
            # We check previous_index because index has already been updated to NextVar
            if previous_index != routing.Start(vehicle_id):
                loc_name = df_loc.iloc[node_index]['Nombre'] if 'Nombre' in df_loc.columns else f"Loc {node_index}"
                client_name = df_loc.iloc[node_index]['Habla a'] if 'Habla a' in df_loc.columns else ""
                lat = df_loc.iloc[node_index]['Latitud (y)']
                lon = df_loc.iloc[node_index]['Longitud (x)']
                
                results.append({
                    'VehicleID': vehicle_id,
                    'NodeID': node_index,
                    'LocationName': loc_name,
                    'Client': client_name,
                    'Latitude': lat,
                    'Longitude': lon,
                    'Load': route_load,
                    'OrderInRoute': len(route_nodes), # adjusted index since we skip start
                    'AccumulatedDuration_Mins': int(route_duration / 60)
                })

            route_nodes.append(node_index)
            route_coords.append((df_loc.iloc[node_index]['Latitud (y)'], df_loc.iloc[node_index]['Longitud (x)']))
            
        # Return to depot (visual)
        node_index = manager.IndexToNode(index) 
        lat = df_loc.iloc[node_index]['Latitud (y)']
        lon = df_loc.iloc[node_index]['Longitud (x)']
        route_coords.append((lat, lon))
        
        total_duration += route_duration
        total_load += route_load
        
        route_maps_data.append({
            'vehicle_id': vehicle_id,
            'coords': route_coords,
            'load': route_load,
            'duration_s': route_duration
        })
        
    return results, route_maps_data, total_duration, total_load

def generate_folium_map(df_loc, route_maps_data):
    """Generates Folium map object"""
    center_lat = df_loc.iloc[0]['Latitud (y)']
    center_lon = df_loc.iloc[0]['Longitud (x)']
    m = folium.Map(location=[center_lat, center_lon], zoom_start=6)
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 
              'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'pink', 'gray', 'black']
    
    # Plot routes
    for r_data in route_maps_data:
        vid = r_data['vehicle_id']
        coords = r_data['coords']
        color = colors[vid % len(colors)]
        
        folium.PolyLine(coords, color=color, weight=3, opacity=0.8).add_to(m)
        
        # Plot markers (except last one which is return to depot, redundant for markers)
        # Actually loop through coordinates to place markers
        for i, (lat, lon) in enumerate(coords[:-1]): 
            # We don't have the node name easily here without re-querying df_loc or passing it down
            # Simplification: Just put a dot
            folium.CircleMarker(
                location=[lat, lon],
                radius=3,
                color=color,
                fill=True,
                fill_color=color,
                popup=f"V{vid}"
            ).add_to(m)

    return m

def solve_vrp_file():
    """Legacy function to run from file as before"""
    print(f"Reading file: {INPUT_FILE}")
    try:
        df_loc = pd.read_excel(INPUT_FILE, sheet_name='1 ubicaciones')
        df_loc.columns = df_loc.columns.str.strip()
        
        # --- LIMPIEZA DE DATOS ---
        print(f"Filas originales: {len(df_loc)}")
        
        # 1. Convertir a numérico forzando errores a NaN
        for col in ['Latitud (y)', 'Longitud (x)']:
            if col in df_loc.columns:
                df_loc[col] = pd.to_numeric(df_loc[col], errors='coerce')
        
        # 2. Eliminar filas con NaN en coordenadas
        valid_rows = df_loc.dropna(subset=['Latitud (y)', 'Longitud (x)'])
        dropped = len(df_loc) - len(valid_rows)
        if dropped > 0:
            print(f"Advertencia: Se eliminaron {dropped} filas con coordenadas inválidas (texto o vacío).")
        df_loc = valid_rows.copy()
        
        # 3. Filtrar coordenadas fuera de rango (Perú aprox: Lat -20 a 0, Lon -82 a -68)
        # Esto ayuda a filtrar errores como -120 o -700
        mask_peru = (
            (df_loc['Latitud (y)'] > -20) & (df_loc['Latitud (y)'] < 0) &
            (df_loc['Longitud (x)'] > -85) & (df_loc['Longitud (x)'] < -65)
        )
        out_of_bounds = df_loc[~mask_peru]
        if not out_of_bounds.empty:
            print(f"Advertencia: Se eliminaron {len(out_of_bounds)} filas con coordenadas fuera de Perú:")
            # print(out_of_bounds[['Nombre', 'Latitud (y)', 'Longitud (x)']].head())
            df_loc = df_loc[mask_peru].copy()

        print(f"Filas válidas para optimizar: {len(df_loc)}")
        # -------------------------
        
        # --- NUEVO REQUERIMIENTO: FIJAR DEPOT EN LA RAMBLA SAN BORJA ---
        # Coordenadas: -12.0884681,-77.0061123
        depot_row = pd.DataFrame([{
            'Nombre': 'La Rambla San Borja',
            'Habla a': 'SODEXO', 
            'Latitud (y)': -12.0884681,
            'Longitud (x)': -77.0061123,
            'Importe de la entrega': 0,
            'Tickets': 0
        }])
        
        # Concatenar al inicio
        df_loc = pd.concat([depot_row, df_loc], ignore_index=True)
        print("Depot fijado en: La Rambla San Borja (-12.0884681, -77.0061123)")
        # -------------------------------------------------------------
        
        # vehicles config from file... simplified usage for now or reimplement full read
        # For backward compatibility, I'll attempt to minimally reconstruct the vehicle logic
        # OR just use the new generic solver with defaults if that suffices?
        # The user's original request implies moving AWAY from the hardcoded file, but keeping the CLI working is nice.
        
        # Let's read the vehicles sheet to get count/cap
        df_veh = pd.read_excel(INPUT_FILE, sheet_name='3.Vehículos')
        df_veh.columns = df_veh.columns.str.strip()
        
        # Simple extraction of total vehicles and max capacity for the generic solver
        total_vehicles = 0
        max_cap = 0
        for _, row in df_veh.iterrows():
            count = int(row.get('Numero de vehiculos', 1))
            cap = int(row.get('Capacidad', 100))
            total_vehicles += count
            max_cap = max(max_cap, cap)
            
        if total_vehicles == 0: total_vehicles = 5
        if max_cap == 0: max_cap = 100
        
        solution, routing, manager, data, df_loc_solved = solve_vrp_data(df_loc, total_vehicles, max_cap)
        
        if solution:
            results, route_data, dist, load = format_solution(data, manager, routing, solution, df_loc_solved)
            
            print(f"Total Distance: {dist}m")
            print(f"Total Load: {load}")
            
            # Save excel
            pd.DataFrame(results).to_excel(OUTPUT_EXCEL, index=False)
            print(f"Saved {OUTPUT_EXCEL}")
            
            # Save map
            m = generate_folium_map(df_loc, route_data)
            m.save(OUTPUT_MAP)
            print(f"Saved {OUTPUT_MAP}")
        else:
            print("No solution found.")
            
    except Exception as e:
        print(f"Error executing legacy mode: {e}")

if __name__ == '__main__':
    solve_vrp_file()
