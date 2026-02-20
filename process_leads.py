import json

def generate_tactical_data():
    # Tactical Colors (Hoodmaps style)
    # RED: Crime/Risk/Industrial
    # YELLOW: Core Growth/Transitional/Speculative
    # GREEN: Elite/Yield/University
    
    COLORS = {
        "ELITE": "#2ed573",       # Green
        "CORE_GROWTH": "#ffa502", # Yellow/Gold
        "STABILITY": "#5f27cd",    # Purple (Uni)
        "SPECULATIVE": "#ff7f50",  # Coral/Orange
        "HIGH_RISK": "#ff4757",    # Red
        "NORMIE": "#1e90ff",       # Blue
        "INDUSTRIAL": "#2f3542"    # Dark Grey
    }

    features = []

    # 1. DEFINE ZONES (Polygons)
    # ELITE (South-West Pioneer)
    features.append({
        "type": "Feature",
        "properties": {"name": "Elite Zone", "color": COLORS["ELITE"], "label": "<b>ELITE (Pioneer)</b><br>High owner-occupancy. Low risk."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.965, 35.035], [-97.945, 35.035], [-97.945, 35.020], [-97.965, 35.020], [-97.965, 35.035]
        ]]}
    })

    # UNIVERSITY HALO
    features.append({
        "type": "Feature",
        "properties": {"name": "USAO Halo", "color": COLORS["STABILITY"], "label": "<b>STABILITY (Uni)</b><br>Student/Faculty anchor. Low vacancy."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.955, 35.045], [-97.935, 35.045], [-97.935, 35.035], [-97.955, 35.035], [-97.955, 35.045]
        ]]}
    })

    # CORE GROWTH (Hwy 62 Corridor)
    features.append({
        "type": "Feature",
        "properties": {"name": "Core Growth", "color": COLORS["CORE_GROWTH"], "label": "<b>CORE GROWTH</b><br>Stable mid-market. Sweet spot for rentals."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.935, 35.055], [-97.915, 35.055], [-97.915, 35.040], [-97.935, 35.040], [-97.935, 35.055]
        ]]}
    })

    # SPECULATIVE (North/Transitional)
    features.append({
        "type": "Feature",
        "properties": {"name": "Speculative Zone", "color": COLORS["SPECULATIVE"], "label": "<b>SPECULATIVE</b><br>Rehab dependent. Block-by-block variance."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.965, 35.065], [-97.935, 35.065], [-97.935, 35.055], [-97.965, 35.055], [-97.965, 35.065]
        ]]}
    })

    # HIGH RISK (3rd St Strip / East Side)
    features.append({
        "type": "Feature",
        "properties": {"name": "High Risk Zone", "color": COLORS["HIGH_RISK"], "label": "<b>HIGH RISK / YIELD</b><br>Industrial blight. Management intensive."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.925, 35.075], [-97.900, 35.075], [-97.900, 35.045], [-97.925, 35.045], [-97.925, 35.075]
        ]]}
    })

    # 2. DEFINE PORTFOLIO (Points)
    PORTFOLIO = [
        {"name": "1922 S 21st St", "coords": [-97.958, 35.028], "type": "portfolio", "zone": "ELITE"},
        {"name": "728 S 17th St", "coords": [-97.952, 35.042], "type": "portfolio", "zone": "CORE_GROWTH"},
        {"name": "1219 W Colorado", "coords": [-97.948, 35.058], "type": "portfolio", "zone": "SPECULATIVE"},
        {"name": "925 S 3rd St", "coords": [-97.918, 35.048], "type": "portfolio", "zone": "HIGH_RISK"}
    ]

    for p in PORTFOLIO:
        features.append({
            "type": "Feature",
            "properties": {
                "name": p["name"],
                "color": "#000000",
                "type": "portfolio",
                "label": f"<b>PORTFOLIO: {p['name']}</b><br>Zone: {p['zone']}"
            },
            "geometry": {"type": "Point", "coordinates": p["coords"]}
        })

    # 3. DEFINE POIS (Tags)
    POIS = [
        {"name": "USAO University", "coords": [-97.9472, 35.0381]},
        {"name": "Leg Lamp", "coords": [-97.9252, 35.0518]},
        {"name": "Walmart", "coords": [-97.9180, 35.0650]},
        {"name": "Shannon Springs Park", "coords": [-97.9355, 35.0395]},
        {"name": "Airport Industrial", "coords": [-97.9680, 35.0920]}
    ]

    for poi in POIS:
        features.append({
            "type": "Feature",
            "properties": {
                "name": poi["name"],
                "type": "poi"
            },
            "geometry": {"type": "Point", "coordinates": poi["coords"]}
        })

    collection = {"type": "FeatureCollection", "features": features}
    with open('projects/maps/data.json', 'w') as f:
        json.dump(collection, f, indent=2)

if __name__ == "__main__":
    generate_tactical_data()
