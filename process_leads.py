import json

def generate_full_coverage_data():
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

    def add_tactical_grid(lon_start, lon_end, lat_start, lat_end, steps_x, steps_y, color, name, label):
        dx = (lon_end - lon_start) / steps_x
        dy = (lat_end - lat_start) / steps_y
        for i in range(steps_x):
            for j in range(steps_y):
                x = lon_start + i * dx
                y = lat_start + j * dy
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

    # 1. ELITE (SW Pioneer) - Expanded South to include the reservoir area
    add_tactical_grid(-97.970, -97.940, 35.005, 35.035, 15, 15, COLORS["ELITE"], "Elite Block", "<b>ELITE</b>")

    # 2. USAO HALO (Stability)
    add_tactical_grid(-97.950, -97.935, 35.035, 35.048, 8, 8, COLORS["STABILITY"], "Stability Block", "<b>STABILITY</b>")

    # 3. CORE GROWTH (Downtown/Mid-Market) - Expanded to fill the center "gap"
    add_tactical_grid(-97.940, -97.920, 35.040, 35.055, 12, 12, COLORS["CORE_GROWTH"], "Core Block", "<b>CORE GROWTH</b>")

    # 4. NORMIES (Stable Mid) - Filling the western gap between Pioneer and Colorado
    add_tactical_grid(-97.970, -97.940, 35.035, 35.055, 15, 10, COLORS["NORMIE"], "Normie Block", "<b>NORMIE</b>")

    # 5. SPECULATIVE (North Side)
    add_tactical_grid(-97.970, -97.930, 35.055, 35.075, 18, 10, COLORS["SPECULATIVE"], "Speculative Block", "<b>SPECULATIVE</b>")

    # 6. HIGH RISK (3rd St Corridor)
    add_tactical_grid(-97.925, -97.910, 35.045, 35.080, 8, 20, COLORS["HIGH_RISK"], "High Risk Block", "<b>HIGH RISK</b>")

    # 7. INDUSTRIAL SLOP
    add_tactical_grid(-97.910, -97.890, 35.045, 35.080, 8, 20, COLORS["INDUSTRIAL"], "Industrial Block", "<b>INDUSTRIAL SLOP</b>")

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
            "properties": {"name": p["name"], "color": "#000", "type": "portfolio", "label": f"<b>PORTFOLIO: {p['name']}</b>"},
            "geometry": {"type": "Point", "coordinates": p["coords"]}
        })

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
    generate_full_coverage_data()
