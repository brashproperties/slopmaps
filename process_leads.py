import json

def generate_block_data():
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

    # Helper to generate a grid of "blocks"
    def add_grid(lon_start, lon_end, lat_start, lat_end, steps_x, steps_y, color, name, label):
        dx = (lon_end - lon_start) / steps_x
        dy = (lat_end - lat_start) / steps_y
        for i in range(steps_x):
            for j in range(steps_y):
                x = lon_start + i * dx
                y = lat_start + j * dy
                # Add slight padding to look like "blocks" with gaps
                gap = 0.0002
                coords = [[
                    [x + gap, y + gap],
                    [x + dx - gap, y + gap],
                    [x + dx - gap, y + dy - gap],
                    [x + gap, y + dy - gap],
                    [x + gap, y + gap]
                ]]
                features.append({
                    "type": "Feature",
                    "properties": {"name": name, "color": color, "label": label},
                    "geometry": {"type": "Polygon", "coordinates": coords}
                })

    # 1. ELITE (South-West) - High density blocks
    add_grid(-97.965, -97.940, 35.015, 35.035, 10, 8, COLORS["ELITE"], "Elite Block", "<b>ELITE</b><br>South-West Pioneer area.")

    # 2. USAO HALO (Stability)
    add_grid(-97.955, -97.935, 35.035, 35.048, 8, 5, COLORS["STABILITY"], "Stability Block", "<b>STABILITY</b><br>University district.")

    # 3. CORE GROWTH (Mid-town)
    add_grid(-97.940, -97.915, 35.040, 35.060, 10, 8, COLORS["CORE_GROWTH"], "Core Block", "<b>CORE GROWTH</b><br>Stable mid-market.")

    # 4. SPECULATIVE (North)
    add_grid(-97.965, -97.930, 35.060, 35.075, 12, 6, COLORS["SPECULATIVE"], "Speculative Block", "<b>SPECULATIVE</b><br>North-side transition.")

    # 5. HIGH RISK (East/Industrial)
    add_grid(-97.915, -97.895, 35.035, 35.075, 8, 15, COLORS["HIGH_RISK"], "High Risk Block", "<b>HIGH RISK</b><br>East side / Industrial.")

    # 6. PORTFOLIO (Points)
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

    # 7. POIS (Tags)
    POIS = [
        {"name": "USAO University", "coords": [-97.9472, 35.0381]},
        {"name": "Leg Lamp", "coords": [-97.9252, 35.0518]},
        {"name": "Walmart", "coords": [-97.9180, 35.0650]},
        {"name": "Shannon Springs Park", "coords": [-97.9355, 35.0395]}
    ]
    for poi in POIS:
        features.append({
            "type": "Feature",
            "properties": {"name": poi["name"], "type": "poi"},
            "geometry": {"type": "Point", "coordinates": poi["coords"]}
        })

    collection = {"type": "FeatureCollection", "features": features}
    with open('projects/maps/data.json', 'w') as f:
        json.dump(collection, f, indent=2)

if __name__ == "__main__":
    generate_block_data()
