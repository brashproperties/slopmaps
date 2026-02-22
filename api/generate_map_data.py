
import json
import os
import random
try:
    from .tactical_logic import TACTICAL_TIERS
except ImportError:
    TACTICAL_TIERS = None

REAL_DATA_PATH = os.path.join(os.path.dirname(__file__), "real_property_data.json")

CHICKASHA_BOUNDING_BOXES = {
    "ELITE": {
        "lat_min": 35.030, "lat_max": 35.060,
        "lon_min": -97.970, "lon_max": -97.940,
    },
    "CORE_GROWTH": {
        "lat_min": 35.060, "lat_max": 35.080,
        "lon_min": -97.950, "lon_max": -97.920,
    },
    "STABILITY": {
        "lat_min": 35.040, "lat_max": 35.055,
        "lon_min": -97.950, "lon_max": -97.930,
    },
    "SPECULATIVE": {
        "lat_min": 35.070, "lat_max": 35.090,
        "lon_min": -97.960, "lon_max": -97.930,
    },
    "HIGH_YIELD_RISK": {
        "lat_min": 35.020, "lat_max": 35.040,
        "lon_min": -97.940, "lon_max": -97.900,
    }
}

def load_real_property_data():
    """Load real property data from the JSON file."""
    if os.path.exists(REAL_DATA_PATH):
        with open(REAL_DATA_PATH, "r") as f:
            return json.load(f)
    return None

def get_base_tier(lat, lon):
    """Determine tier based on location within bounding boxes."""
    for tier_name, bbox in CHICKASHA_BOUNDING_BOXES.items():
        if bbox["lat_min"] <= lat <= bbox["lat_max"] and \
           bbox["lon_min"] <= lon <= bbox["lon_max"]:
            return tier_name
    return "SPECULATIVE"

def generate_map_data(grid_size=(100, 100), output_dir=".", use_real_data=True):
    """
    Generates granular map data for Chickasha with real property data in GeoJSON format.
    """
    features = []
    
    real_data = load_real_property_data() if use_real_data else None
    
    if real_data and "properties" in real_data:
        prop_data = real_data["properties"]
        for i, prop in enumerate(prop_data):
            lat = prop.get("lat")
            lon = prop.get("lon")
            if lat is None or lon is None:
                continue
            
            estimated_value = prop.get("estimated_value", 0)
            sale_price = prop.get("sale_price", 0)
            square_footage = prop.get("square_footage", 0)
            vacancy_indicator = prop.get("vacancy_indicator", False)
            
            vacancy_rate = 15.0 if vacancy_indicator else 5.0
            
            sqft = square_footage if square_footage > 0 else 1000
            price_per_sqft = estimated_value / sqft if sqft > 0 else 100
            
            crime_rate = max(0, min(10, 5 + random.uniform(-2, 2)))
            
            property_value_normalized = min(1.0, estimated_value / 350000)
            vibe_score = (property_value_normalized * 0.5) + ((10 - crime_rate) * 0.3) + ((20 - vacancy_rate) * 0.2)
            vibe_score = round(vibe_score, 2)
            
            if vibe_score >= 8.0:
                color = "#96c93d"
            elif vibe_score >= 6.5:
                color = "#feca57"
            elif vibe_score >= 5.0:
                color = "#54a0ff"
            elif vibe_score >= 3.5:
                color = "#ff9900"
            else:
                color = "#ff6b6b"
            
            tier = get_base_tier(lat, lon)
            
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [lon, lat]
                },
                "properties": {
                    "id": f"real-{i}",
                    "tier": tier,
                    "vibe_score": vibe_score,
                    "property_value": int(estimated_value),
                    "sale_price": int(sale_price),
                    "square_footage": int(square_footage),
                    "crime_rate": round(crime_rate, 1),
                    "vacancy_rate": round(vacancy_rate, 1),
                    "vacancy_indicator": vacancy_indicator,
                    "color": color,
                    "label": f"Vibe: {vibe_score}/10 | ${int(estimated_value/1000)}k | {int(square_footage)}ft²"
                }
            }
            features.append(feature)
        
        print(f"Loaded {len(features)} real property records")
    else:
        center_lat = 35.0526
        center_lon = -97.9364
        lat_span = 0.10
        lon_span = 0.10

        lat_step = lat_span / grid_size[0]
        lon_step = lon_span / grid_size[1]

        for i in range(grid_size[0]):
            for j in range(grid_size[1]):
                lat = center_lat - (lat_span / 2) + (i * lat_step)
                lon = center_lon - (lon_span / 2) + (j * lon_step)

                tier = get_base_tier(lat, lon)

                if tier == "ELITE":
                    base_value = random.uniform(150000, 300000)
                    base_crime = random.uniform(0, 3)
                    base_vacancy = random.uniform(0, 5)
                elif tier == "CORE_GROWTH":
                    base_value = random.uniform(100000, 180000)
                    base_crime = random.uniform(2, 6)
                    base_vacancy = random.uniform(5, 12)
                elif tier == "STABILITY":
                    base_value = random.uniform(120000, 200000)
                    base_crime = random.uniform(1, 5)
                    base_vacancy = random.uniform(3, 8)
                elif tier == "SPECULATIVE":
                    base_value = random.uniform(60000, 120000)
                    base_crime = random.uniform(4, 8)
                    base_vacancy = random.uniform(8, 15)
                elif tier == "HIGH_YIELD_RISK":
                    base_value = random.uniform(30000, 80000)
                    base_crime = random.uniform(6, 10)
                    base_vacancy = random.uniform(10, 20)
                else:
                    base_value = random.uniform(50000, 150000)
                    base_crime = random.uniform(3, 8)
                    base_vacancy = random.uniform(5, 15)

                property_value = base_value * random.uniform(0.9, 1.1)
                crime_rate = max(0, min(10, base_crime * random.uniform(0.8, 1.2)))
                vacancy_rate = max(0, min(20, base_vacancy * random.uniform(0.8, 1.2)))

                property_value_normalized = min(1.0, property_value / 300000)
                vibe_score = (property_value_normalized * 0.5) + ((10 - crime_rate) * 0.3) + ((20 - vacancy_rate) * 0.2)
                vibe_score = round(vibe_score, 2)

                if vibe_score >= 8.0:
                    color = "#96c93d"
                elif vibe_score >= 6.5:
                    color = "#feca57"
                elif vibe_score >= 5.0:
                    color = "#54a0ff"
                elif vibe_score >= 3.5:
                    color = "#ff9900"
                else:
                    color = "#ff6b6b"

                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "id": f"{i}-{j}",
                        "tier": tier,
                        "vibe_score": vibe_score,
                        "property_value": int(property_value),
                        "crime_rate": round(crime_rate, 1),
                        "vacancy_rate": round(vacancy_rate, 1),
                        "color": color,
                        "label": f"Vibe: {vibe_score}/10 | ${int(property_value)}k"
                    }
                }
                features.append(feature)

    geojson_data = {
        "type": "FeatureCollection",
        "features": features
    }

    output_path = os.path.join(output_dir, "data.json")
    with open(output_path, "w") as f:
        json.dump(geojson_data, f, indent=2)
    print(f"Generated map data to {output_path} ({len(features)} features)")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_map_data(output_dir=current_dir)
