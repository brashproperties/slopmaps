#!/usr/bin/env python3
"""
Indiana Map Generator for Brash Properties Slopmap
Creates geoJSON data for Evansville, Mt Vernon, and Newburgh
"""

import json
import math

# City center approximate coordinates
CITIES = {
    "evansville": {"lat": 37.9772, "lng": -87.5506, "zoom": 13},
    "mt_vernon": {"lat": 37.932, "lng": -87.895, "zoom": 14},
    "newburgh": {"lat": 37.9471, "lng": -87.4003, "zoom": 14}
}

# Property addresses with approximate coordinates (from search + estimation)
# Evansville properties
EVANSVILLE_PROPERTIES = [
    {"address": "1200-1204 1st St", "lat": 37.9585, "lng": -87.5780},  # East side near river
    {"address": "20 E Campground Rd", "lat": 37.9650, "lng": -87.5400},  # Near Haynie's Corner area
    {"address": "2416 Margybeth", "lat": 37.9900, "lng": -87.5350},  # North side
    {"address": "1805 N Main St", "lat": 37.9850, "lng": -87.5700},  # North Main area
    {"address": "920 Canal St", "lat": 37.9550, "lng": -87.5750},  # Downtown/Canal area
    {"address": "921 W Oregon", "lat": 37.9650, "lng": -87.5850},  # West side
    {"address": "908 N 1st Ave", "lat": 37.9780, "lng": -87.5680},  # North 1st area
    {"address": "703 E Columbia A/B", "lat": 37.9520, "lng": -87.5550},  # Columbia area
    {"address": "515 S Grand St", "lat": 37.9550, "lng": -87.5900},  # South side
    {"address": "1320 N Fares", "lat": 37.9820, "lng": -87.5450},  # North Fares
    {"address": "230 W 3rd St", "lat": 37.9600, "lng": -87.5800},  # West 3rd
    {"address": "2004 S Taft", "lat": 37.9450, "lng": -87.5650},  # South Taft
    {"address": "220 NW 4th", "lat": 37.9650, "lng": -87.5820},  # NW 4th area
]

# Mt Vernon properties  
MT_VERNON_PROPERTIES = [
    {"address": "311 Vine St", "lat": 37.9340, "lng": -87.8980},  # Downtown
    {"address": "354/358 Audubon", "lat": 37.9280, "lng": -87.8900},  # Audubon area
    {"address": "527-531 W 2nd", "lat": 37.9360, "lng": -87.9020},  # West 2nd
    {"address": "Kimball", "lat": 37.9400, "lng": -87.8850},  # Kimball area
    {"address": "9th St", "lat": 37.9250, "lng": -87.9000},  # 9th St
    {"address": "619 College Avenue", "lat": 37.9380, "lng": -87.8920},  # College Ave
    {"address": "721 Smith Rd", "lat": 37.9450, "lng": -87.8800},  # Smith Rd area
]

# Newburgh properties
NEWBURGH_PROPERTIES = [
    {"address": "6697 Concord Dr", "lat": 37.9480, "lng": -87.4050},  # Concord Dr area
]

# Landmarks
LANDMARKS = [
    {"name": "Deaconess Hospital", "lat": 37.9834, "lng": -87.5708, "type": "hospital"},
    {"name": "University of Evansville", "lat": 37.9716, "lng": -87.5317, "type": "university"},
    {"name": "Victory Temple", "lat": 37.9630, "lng": -87.5550, "type": "church"},
    {"name": "Ohio River", "lat": 37.9500, "lng": -87.6000, "type": "river"},
]

# Zone definitions - approximate polygons
# Format: [min_lat, max_lat, min_lng, max_lng, color, label]

# Evansville zones
EVANSVILLE_ZONES = [
    # Best zones (green - appreciation/rich)
    {"name": "Haynie's Corner", "color": "#2ed573", "bounds": [37.955, 37.970, -87.580, -87.560]},
    {"name": "North Park", "color": "#2ed573", "bounds": [37.985, 38.000, -87.560, -87.530]},
    {"name": "Melody Hill", "color": "#2ed573", "bounds": [37.975, 37.990, -87.520, -87.500]},
    {"name": "Jacobsville", "color": "#2ed573", "bounds": [37.965, 37.980, -87.540, -87.520]},
    
    # Good zones (yellow - cash flow/yield)
    {"name": "McCutchanville", "color": "#ffa502", "bounds": [37.990, 38.010, -87.550, -87.520]},
    {"name": "Lamasco", "color": "#ffa502", "bounds": [37.950, 37.965, -87.550, -87.535]},
    {"name": "Oaklyn", "color": "#ffa502", "bounds": [37.975, 37.985, -87.565, -87.545]},
    
    # Bad zones (red - avoid/high crime, industrial)
    {"name": "West Side Industrial", "color": "#2f3542", "bounds": [37.955, 37.975, -87.600, -87.570]},
]

# Mt Vernon zones
MT_VERNON_ZONES = [
    # Best (central/downtown)
    {"name": "Downtown Mt Vernon", "color": "#2ed573", "bounds": [37.928, 37.940, -87.910, -87.885]},
    
    # Good (Tanglewood, Kennedy)
    {"name": "Tanglewood", "color": "#ffa502", "bounds": [37.935, 37.950, -87.900, -87.880]},
    {"name": "Kennedy", "color": "#ffa502", "bounds": [37.920, 37.935, -87.890, -87.870]},
    
    # Bad (rural outskirts)
    {"name": "Rural Outskirts", "color": "#ff4757", "bounds": [37.900, 37.950, -87.950, -87.850]},
]

# Newburgh zones
NEWBURGH_ZONES = [
    # Best
    {"name": "Berkshire", "color": "#2ed573", "bounds": [37.940, 37.955, -87.420, -87.400]},
    {"name": "South Broadview", "color": "#2ed573", "bounds": [37.935, 37.948, -87.415, -87.395]},
    {"name": "Fall Creek", "color": "#2ed573", "bounds": [37.950, 37.965, -87.410, -37.890]},  # Fixed
     
    # Good
    {"name": "Old Hickory", "color": "#ffa502", "bounds": [37.938, 37.950, -87.440, -87.420]},
    {"name": "Green Springs", "color": "#ffa502", "bounds": [37.955, 37.970, -87.400, -87.380]},
]

def create_grid_polygons(zones):
    """Create grid polygons from zone bounds"""
    features = []
    for zone in zones:
        bounds = zone["bounds"]
        # Create a simple polygon for each zone
        # Using small grid cells within the bounds
        min_lat, max_lat, min_lng, max_lng = bounds
        
        # Handle the Fall Creek issue
        if max_lng < min_lng:
            max_lng = -87.380  # Fix the coordinate
            
        # Create multiple small polygons (grid cells)
        lat_step = (max_lat - min_lat) / 3
        lng_step = (max_lng - min_lng) / 3
        
        for i in range(3):
            for j in range(3):
                cell_min_lat = min_lat + i * lat_step
                cell_max_lat = cell_min_lat + lat_step
                cell_min_lng = min_lng + j * lng_step
                cell_max_lng = cell_min_lng + lng_step
                
                feature = {
                    "type": "Feature",
                    "properties": {
                        "name": zone["name"],
                        "color": zone["color"],
                        "type": "tactical_block"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [cell_min_lng, cell_min_lat],
                            [cell_max_lng, cell_min_lat],
                            [cell_max_lng, cell_max_lat],
                            [cell_min_lng, cell_max_lat],
                            [cell_min_lng, cell_min_lat]
                        ]]
                    }
                }
                features.append(feature)
    return features

def create_portfolio_pins(properties, city):
    """Create portfolio pin features"""
    features = []
    for prop in properties:
        feature = {
            "type": "Feature",
            "properties": {
                "name": prop["address"],
                "type": "portfolio",
                "city": city
            },
            "geometry": {
                "type": "Point",
                "coordinates": [prop["lng"], prop["lat"]]
            }
        }
        features.append(feature)
    return features

def create_landmarks(landmarks):
    """Create landmark features"""
    features = []
    for lm in landmarks:
        feature = {
            "type": "Feature",
            "properties": {
                "name": lm["name"],
                "type": "poi",
                "subtype": lm["type"]
            },
            "geometry": {
                "type": "Point",
                "coordinates": [lm["lng"], lm["lat"]]
            }
        }
        features.append(feature)
    return features

def main():
    features = []
    
    # Add zone polygons
    features.extend(create_grid_polygons(EVANSVILLE_ZONES))
    features.extend(create_grid_polygons(MT_VERNON_ZONES))
    features.extend(create_grid_polygons(NEWBURGH_ZONES))
    
    # Add portfolio pins
    features.extend(create_portfolio_pins(EVANSVILLE_PROPERTIES, "Evansville"))
    features.extend(create_portfolio_pins(MT_VERNON_PROPERTIES, "Mt Vernon"))
    features.extend(create_portfolio_pins(NEWBURGH_PROPERTIES, "Newburgh"))
    
    # Add landmarks
    features.extend(create_landmarks(LANDMARKS))
    
    # Create the FeatureCollection
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Write to data file
    with open('/home/clawdbot/projects/maps/data_indiana.json', 'w') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Generated {len(features)} features")
    print(f"  - Zones: {len(EVANSVILLE_ZONES)*9 + len(MT_VERNON_ZONES)*9 + len(NEWBURGH_ZONES)*9}")
    print(f"  - Portfolio pins: {len(EVANSVILLE_PROPERTIES) + len(MT_VERNON_PROPERTIES) + len(NEWBURGH_PROPERTIES)}")
    print(f"  - Landmarks: {len(LANDMARKS)}")

if __name__ == "__main__":
    main()
