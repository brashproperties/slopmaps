import json

def generate_tactical_data():
    COLORS = {
        "ELITE": "#2ed573",       # Green (Appreciation / Rich)
        "CORE_GROWTH": "#ffa502", # Yellow (Cash Flow / Yield)
        "STABILITY": "#5f27cd",    # Purple (Uni / Students)
        "SPECULATIVE": "#ff7f50",  # Orange (Speculative)
        "HIGH_RISK": "#ff4757",    # Red (Avoid / High Crime)
        "NORMIE": "#1e90ff",       # Blue (Owner-Occupant / Stable)
        "INDUSTRIAL": "#2f3542"    # Grey (Industrial Slop)
    }

    features = []

    # 1. ELITE (Pioneer/Southwest)
    # Boundaries: South of Alabama Ave, West of 17th St down to Country Club Rd
    features.append({
        "type": "Feature",
        "properties": {"name": "Elite (Pioneer)", "color": COLORS["ELITE"], "label": "<b>ELITE</b><br>High owner-occupancy. Best schools. Low risk."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.970, 35.035], [-97.945, 35.035], [-97.945, 35.015], [-97.970, 35.015], [-97.970, 35.035]
        ]]}
    })

    # 2. USAO HALO (Stability)
    # Boundaries: Around 17th to 9th, Iowa to Grand
    features.append({
        "type": "Feature",
        "properties": {"name": "USAO / University District", "color": COLORS["STABILITY"], "label": "<b>STABILITY (Uni)</b><br>Student/Faculty anchor. Reliable rental demand."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.955, 35.045], [-97.935, 35.045], [-97.935, 35.035], [-97.955, 35.035], [-97.955, 35.045]
        ]]}
    })

    # 3. CORE GROWTH (Downtown/Mid-Market)
    # Boundaries: Grand Ave to Choctaw Ave, 9th St to 1st St
    features.append({
        "type": "Feature",
        "properties": {"name": "Core Growth (Downtown)", "color": COLORS["CORE_GROWTH"], "label": "<b>CORE GROWTH</b><br>Revitalization zone. High rental yield potential."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.935, 35.055], [-97.925, 35.055], [-97.925, 35.040], [-97.935, 35.040], [-97.935, 35.055]
        ]]}
    })

    # 4. NORMIE (Owner-Occupant / Middle Class)
    # Boundaries: West of 17th, North of Alabama up to Colorado
    features.append({
        "type": "Feature",
        "properties": {"name": "Normie Belt", "color": COLORS["NORMIE"], "label": "<b>NORMIES</b><br>Standard middle-class neighborhoods. Low appreciation, high stability."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.965, 35.050], [-97.945, 35.050], [-97.945, 35.035], [-97.965, 35.035], [-97.965, 35.050]
        ]]}
    })

    # 5. SPECULATIVE (North Chickasha)
    # Boundaries: North of Grand Ave, West side of town
    features.append({
        "type": "Feature",
        "properties": {"name": "Speculative North", "color": COLORS["SPECULATIVE"], "label": "<b>SPECULATIVE</b><br>Rehab heavy. Block-by-block risk/reward."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.965, 35.065], [-97.935, 35.065], [-97.935, 35.055], [-97.965, 35.055], [-97.965, 35.065]
        ]]}
    })

    # 6. HIGH RISK (3rd St Corridor / East)
    # Boundaries: East of 4th St, North of Choctaw
    features.append({
        "type": "Feature",
        "properties": {"name": "High Risk / 3rd St", "color": COLORS["HIGH_RISK"], "label": "<b>HIGH RISK</b><br>Heavy blight. High crime indicators. Avoid or extreme yield."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.925, 35.075], [-97.910, 35.075], [-97.910, 35.045], [-97.925, 35.045], [-97.925, 35.075]
        ]]}
    })

    # 7. INDUSTRIAL SLOP
    # Boundaries: Far East side near tracks/turnpike
    features.append({
        "type": "Feature",
        "properties": {"name": "Industrial Slop", "color": COLORS["INDUSTRIAL"], "label": "<b>INDUSTRIAL SLOP</b><br>Non-residential/Commercial blight."},
        "geometry": {"type": "Polygon", "coordinates": [[
            [-97.910, 35.075], [-97.895, 35.075], [-97.895, 35.045], [-97.910, 35.045], [-97.910, 35.075]
        ]]}
    })

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
    generate_tactical_data()
