
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Define Chickasha boundaries (approximate)
# Map center: 35.0526, -97.9359
lats = np.linspace(35.075, 35.015, 10) # North to South
lngs = np.linspace(-97.970, -97.910, 10) # West to East

# Portfolio Pins
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "green"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "yellow"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "orange"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "red"}
]

# Create the figure
fig, ax = plt.subplots(figsize=(12, 10))

# Create a manual gradient background for the heatmap
# North (Top) is Red, South (Bottom) is Green
gradient = np.zeros((10, 10))
for i in range(10):
    gradient[i, :] = i / 9.0  # 0 at top (North), 1 at bottom (South)

# Display the gradient (Red at top, Green at bottom)
im = ax.imshow(gradient, extent=[-97.970, -97.910, 35.015, 35.075], cmap='RdYlGn', alpha=0.3, origin='upper')

# Add street grid (Simplified)
ax.set_title("Brash Properties Tactical Map - Chickasha, OK (73018)", fontsize=16, fontweight='bold')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Plot the properties
for p in properties:
    ax.scatter(p['lng'], p['lat'], color=p['color'], s=200, edgecolors='black', label=p['name'], zorder=5)
    ax.text(p['lng']+0.001, p['lat'], p['name'], fontsize=10, fontweight='bold', zorder=6)

# Add key labels
ax.text(-97.965, 35.065, "NORTH: HIGH RISK", color='red', fontsize=12, fontweight='bold')
ax.text(-97.965, 35.025, "SOUTH: PRIME EQUITY", color='darkgreen', fontsize=12, fontweight='bold')

plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('/home/clawdbot/.openclaw/workspace/chickasha_tactical_map_render.png', dpi=300, bbox_inches='tight')
print("Map rendered successfully.")
