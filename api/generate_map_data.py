
import json
import os
import random
from .tactical_logic import TACTICAL_TIERS # Import from the same package

def generate_map_data(grid_size=(10, 10), output_dir="."):
    """
    Generates dummy map data for Chickasha with vibe scores based on tactical tiers.
    """
    data = []
    # Simplified coordinates for Chickasha area
    base_lat = 35.035
    base_lon = -97.940

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            lat = base_lat + (i * 0.01)  # Increment latitude
            lon = base_lon + (j * 0.01)  # Increment longitude

            # Assign a random tier for now to simulate vibe scores
            tiers = list(TACTICAL_TIERS.keys())
            random_tier_key = random.choice(tiers)
            tier_info = TACTICAL_TIERS[random_tier_key]

            vibe_score = random.uniform(0.1, 1.0) # Dummy vibe score

            data.append({
                "id": f"{i}-{j}",
                "latitude": lat,
                "longitude": lon,
                "vibe_score": vibe_score,
                "tier": random_tier_key,
                "color": tier_info["color"]
            })

    output_path = os.path.join(output_dir, "data.json")
    with open(output_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Generated map data to {output_path}")

if __name__ == "__main__":
    # Ensure this script is run from the parent directory as a module for correct imports
    # python3 -m api.generate_map_data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    generate_map_data(output_dir=current_dir)
