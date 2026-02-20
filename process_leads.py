import json
import os

# Paths
DATA_PATH = 'projects/data/brash_chickasha_master_data.json'
OUTPUT_PATH = 'projects/chickasha_slopmap/web/data.json'

# POIs (Points of Interest) - noteworthy Chickasha landmarks
POIS = [
    {"name": "USAO University", "type": "uni", "lat": 35.0381, "lng": -97.9472, "label": "Uni / Hipsters"},
    {"name": "The Leg Lamp (Downtown)", "type": "tourist", "lat": 35.0518, "lng": -97.9252, "label": "Tourists / Kitsch"},
    {"name": "North Industrial / Food Plants", "type": "suits", "lat": 35.0725, "lng": -97.9205, "label": "Suits / Industrial Slop"},
    {"name": "Shannon Springs Park", "type": "normies", "lat": 35.0395, "lng": -97.9355, "label": "Normies / Park"},
    {"name": "Grady County Fairgrounds", "type": "normies", "lat": 35.0605, "lng": -97.9525, "label": "Normies / Fairgrounds"}
]

# Color Palette (Hoodmaps inspired)
PALETTE = {
    "suits": "#45B7D1", # Blue
    "rich": "#FECA57",   # Yellow/Gold
    "cool": "#FF9FF3",   # Pink
    "tourists": "#FF6B6B", # Reddish
    "uni": "#96C93D",     # Green
    "normies": "#54A0FF", # Light Blue
    "crime": "#5F27CD"    # Purple
}

def generate_grid(lat_min, lat_max, lng_min, lng_max, step=0.005):
    grid = []
    lat = lat_min
    while lat < lat_max:
        lng = lng_min
        while lng < lng_max:
            # Simple heuristic for coloring based on our master data tiers
            # Brash Green -> Rich/Cool
            # Brash Yellow -> Normies/Suits
            # Brash Red -> Crime/Suits
            
            color = PALETTE["normies"]
            label = "Normies"
            
            # Map tiers to Hoodmaps styles
            if lat < 35.045 and lng < -97.935: # Southwest (Univ Heights)
                color = PALETTE["rich"]
                label = "Rich / Uni"
            elif lat > 35.060: # North (Industrial)
                color = PALETTE["suits"]
                label = "Suits / Industrial"
            elif 35.045 < lat < 35.060 and lng > -97.930: # Downtown core
                color = PALETTE["crime"]
                label = "Crime / Hipsters?"
            
            grid.append({
                "type": "Feature",
                "properties": {
                    "color": color,
                    "label": label
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [lng, lat],
                        [lng + step, lat],
                        [lng + step, lat + step],
                        [lng, lat + step],
                        [lng, lat]
                    ]]
                }
            })
            lng += step
        lat += step
    return grid

def process_data():
    features = []
    
    # 1. Generate the Hoodmaps-style Grid
    features.extend(generate_grid(35.020, 35.080, -97.960, -97.910))

    # 2. Add POIs
    for poi in POIS:
        features.append({
            "type": "Feature",
            "properties": {
                "name": poi['name'],
                "color": PALETTE.get(poi['type'], "#000"),
                "type": "poi",
                "label": f"<b>{poi['name']}</b><br>{poi['label']}"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [poi['lng'], poi['lat']]
            }
        })

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(geojson, f, indent=2)
    print(f"Generated Hoodmaps style data with {len(features)} features.")

if __name__ == "__main__":
    process_data()
