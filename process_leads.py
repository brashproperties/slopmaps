import json

def generate_hybrid_data():
    COLORS = {
        "ELITE": "#2ed573",
        "CORE_GROWTH": "#ffa502",
        "STABILITY": "#5f27cd",
        "SPECULATIVE": "#ff7f50",
        "HIGH_RISK": "#ff4757",
        "NORMIE": "#1e90ff",
        "INDUSTRIAL": "#2f3542"
    }

    features = []

    # HELPER: Generate small blocks ONLY inside a defined boundary
    def add_tactical_grid(lon_start, lon_end, lat_start, lat_end, steps_x, steps_y, color, name, label):
        dx = (lon_end - lon_start) / steps_x
        dy = (lat_end - lat_start) / steps_y
        for i in range(steps_x):
            for j in range(steps_y):
                x = lon_start + i * dx
                y = lat_start + j * dy
                # 0.0001 gap for a tight, high-tech grid look
                gap = 0.0001
                coords = [[
                    [x + gap, y + gap],
                    [x + dx - gap, y + gap],
                    [x + dx - gap, y + dy - gap],
                    [x + gap, y + dy - gap],
                    [x + gap, y + gap]
                ]]
                features.append({
                    "type": "Feature",
                    "properties": {"name": name, "color": color, "label": label, "type": "tactical_block"},
                    "geometry": {"type": "Polygon", "coordinates": coords}
                })

    # 1. ELITE (SW Pioneer) - Tight 12x12 grid
    add_tactical_grid(-97.970, -97.945, 35.015, 35.035, 12, 12, COLORS["ELITE"], "Elite Block", "<b>ELITE</b><br>South-West Pioneer area.")

    # 2. USAO HALO (Stability) - 10x10
    add_tactical_grid(-97.955, -97.935, 35.035, 35.048, 10, 10, COLORS["STABILITY"], "Stability Block", "<b>STABILITY</b><br>University district.")

    # 3. CORE GROWTH (Downtown) - 8x12
    add_tactical_grid(-97.935, -97.920, 35.040, 35.055, 8, 12, COLORS["CORE_GROWTH"], "Core Block", "<b>CORE GROWTH</b><br>Stable mid-market.")

    # 4. NORMIES (Stable Mid) - 12x10
    add_tactical_grid(-97.970, -97.945, 35.035, 35.050, 12, 10, COLORS["NORMIE"], "Normie Block", "<b>NORMIE</b><br>Stable middle-class.")

    # 5. SPECULATIVE (North Side) - 15x8
    add_tactical_grid(-97.965, -97.930, 35.055, 35.070, 15, 8, COLORS["SPECULATIVE"], "Speculative Block", "<b>SPECULATIVE</b><br>North-side transition.")

    # 6. HIGH RISK (3rd St Corridor) - 8x20 (Very granular)
    add_tactical_grid(-97.925, -97.910, 35.045, 35.075, 8, 20, COLORS["HIGH_RISK"], "High Risk Block", "<b>HIGH RISK</b><br>East side / Industrial.")

    # 7. INDUSTRIAL SLOP - 6x15
    add_tactical_grid(-97.910, -97.895, 35.045, 35.075, 6, 15, COLORS["INDUSTRIAL"], "Industrial Block", "<b>INDUSTRIAL SLOP</b>")

    # 8. PORTFOLIO
    PORTFOLIO = [
        {"name": "1922 S 21st St", "coords": [-97.958, 35.028], "type": "portfolio", "zone": "ELITE"},
        {"name": "728 S 17th St", "coords": [-97.952, 35.042], "type": "portfolio", "zone": "CORE_GROWTH"},
        {"name": "1219 W Colorado", "coords": [-97.948, 35.058], "type": "portfolio", "zone": "SPECULATIVE"},
        {"name": "925 S 3rd St", "coords": [-97.918, 35.048], "type": "portfolio", "zone": "HIGH_RISK"}
    ]
    for p in PORTFOLIO:
        features.append({
            "type": "Feature",
            "properties": {"name": p["name"], "color": "#000", "type": "portfolio", "label": f"<b>PORTFOLIO: {p['name']}</b><br>Zone: {p['zone']}"},
            "geometry": {"type": "Point", "coordinates": p["coords"]}
        })

    # 9. POIS
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

    with open('projects/maps/data.json', 'w') as f:
        json.dump({"type": "FeatureCollection", "features": features}, f, indent=2)

if __name__ == "__main__":
    generate_hybrid_data()
