import json
import os
import random
import math

REAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "real_property_data.json")

CHICKASHA_BOUNDS = {
    "lat_min": 35.01,
    "lat_max": 35.09,
    "lon_min": -97.98,
    "lon_max": -97.90
}

def load_real_property_data():
    """Load real property data from the JSON file."""
    if os.path.exists(REAL_DATA_PATH):
        with open(REAL_DATA_PATH, "r") as f:
            return json.load(f)
    return None

def distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km."""
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111

def get_properties_in_cell(lat_min, lat_max, lon_min, lon_max, properties):
    """Get all properties within a grid cell."""
    cell_props = []
    for prop in properties:
        lat = prop.get("lat")
        lon = prop.get("lon")
        if lat is None or lon is None:
            continue
        if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
            cell_props.append(prop)
    return cell_props

def get_directional_value(lat, lon):
    """
    Calculate a directional value based on location.
    Southwest (lower lat, lower lon) = higher values
    Northeast (higher lat, higher lon) = lower values
    """
    lat_norm = (lat - CHICKASHA_BOUNDS["lat_min"]) / (CHICKASHA_BOUNDS["lat_max"] - CHICKASHA_BOUNDS["lat_min"])
    lon_norm = (lon - CHICKASHA_BOUNDS["lon_min"]) / (CHICKASHA_BOUNDS["lon_max"] - CHICKASHA_BOUNDS["lon_min"])
    
    # SW = high (1), NE = low (0)
    # Use inverse of lat + inverse of lon for SW-to-NE gradient
    value = 1.0 - ((lat_norm + lon_norm) / 2)
    return value

def calculate_cell_vibe_score(properties_in_cell, lat, lon):
    """
    Calculate composite vibe score (1-10) based on:
    - marketValue/sqft (from property data - higher is better)
    - Directional gradient for cells without property data
    """
    # First check if there are properties in this cell
    if properties_in_cell:
        sqft_prices = []
        market_values = []
        
        for prop in properties_in_cell:
            sqft = prop.get("square_footage", 0) or prop.get("squareFeet", 0)
            # Use marketValue if available, otherwise estimatedValue
            market_value = prop.get("market_value") or prop.get("estimated_value") or prop.get("estimatedValue", 0)
            
            if sqft and sqft > 0 and market_value:
                sqft_prices.append(market_value / sqft)
                market_values.append(market_value)
        
        if sqft_prices:
            avg_sqft_price = sum(sqft_prices) / len(sqft_prices)
            # Normalize: $200/sqft = 10, $40/sqft = 1
            vibe_score = max(1, min(10, (avg_sqft_price - 40) / 16))
            return round(vibe_score, 2), round(avg_sqft_price, 0), len(properties_in_cell)
    
    # No properties in cell - use directional gradient
    # SW = higher values, NE = lower values
    directional_value = get_directional_value(lat, lon)
    
    # Map directional value to vibe score (1-10)
    # directional_value: 1 (SW) -> 10, 0 (NE) -> 1
    base_vibe = 1 + (directional_value * 9)
    
    # Add some variation but keep it smooth
    vibe_score = base_vibe
    
    # Calculate synthetic $/sqft based on direction
    # SW: ~$150/sqft, NE: ~$50/sqft
    avg_sqft_price = 50 + (directional_value * 100)
    
    return round(vibe_score, 2), round(avg_sqft_price, 0), 0

def vibe_to_color(vibe_score):
    """
    Convert vibe score (1-10) to color gradient:
    1 = bright red (#ff0000)
    10 = bright green (#00ff00)
    Smooth gradient in between
    """
    t = (vibe_score - 1) / 9
    
    r = int(255 * (1 - t))
    g = int(255 * t)
    b = 0
    
    return f"#{r:02x}{g:02x}{b:02x}"

def generate_grid_data(grid_size=50, output_dir="."):
    """
    Generate a 50x50 grid overlay for Chickasha with vibe scores.
    Every cell gets a color - no transparent cells.
    Uses directional gradient for cells without property data.
    """
    features = []
    
    real_data = load_real_property_data()
    properties = real_data.get("properties", []) if real_data else []
    
    lat_step = (CHICKASHA_BOUNDS["lat_max"] - CHICKASHA_BOUNDS["lat_min"]) / grid_size
    lon_step = (CHICKASHA_BOUNDS["lon_max"] - CHICKASHA_BOUNDS["lon_min"]) / grid_size
    
    cells_with_properties = 0
    
    for i in range(grid_size):
        for j in range(grid_size):
            lat_min = CHICKASHA_BOUNDS["lat_min"] + i * lat_step
            lat_max = lat_min + lat_step
            lon_min = CHICKASHA_BOUNDS["lon_min"] + j * lon_step
            lon_max = lon_min + lon_step
            
            center_lat = (lat_min + lat_max) / 2
            center_lon = (lon_min + lon_max) / 2
            
            cell_props = get_properties_in_cell(lat_min, lat_max, lon_min, lon_max, properties)
            
            vibe_score, avg_sqft, prop_count = calculate_cell_vibe_score(cell_props, center_lat, center_lon)
            
            if prop_count > 0:
                cells_with_properties += 1
            
            color = vibe_to_color(vibe_score)
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [lon_min, lat_min],
                        [lon_max, lat_min],
                        [lon_max, lat_max],
                        [lon_min, lat_max],
                        [lon_min, lat_min]
                    ]]
                },
                "properties": {
                    "id": f"cell-{i}-{j}",
                    "vibe_score": vibe_score,
                    "avg_sqft_price": int(avg_sqft),
                    "property_count": prop_count,
                    "color": color,
                    "center_lat": center_lat,
                    "center_lon": center_lon
                }
            }
            features.append(feature)
    
    # Convert to GeoJSON format for Leaflet
    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }
    
    output_path = os.path.join(output_dir, "grid_data.json")
    with open(output_path, "w") as f:
        json.dump(geojson_data, f)
    
    print(f"Generated grid data to {output_path}")
    print(f"Grid: {grid_size}x{grid_size} = {len(features)} cells")
    print(f"Cells with properties: {cells_with_properties}")
    print(f"Cells without properties: {len(features) - cells_with_properties} (filled with directional gradient)")
    print(f"Grid bounds: {CHICKASHA_BOUNDS}")
    print(f"Cell size: ~{lat_step*111*1000:.0f}m x {lon_step*111*1000:.0f}m")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    generate_grid_data(grid_size=50, output_dir=parent_dir)
