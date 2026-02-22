
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

# Define Chickasha boundaries for the crop/overlay
# These need to be precise to match the background image if we had one, 
# but for now we'll use a better schematic with major roads.
lats_range = [35.015, 35.075] 
lngs_range = [-97.970, -97.910]

# Portfolio Pins
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "#00FF00"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "#FFD700"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "#FFA500"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "#FF0000"}
]

# Major Roads (Approximated for Schematic Overlay)
roads = [
    {"name": "Grand Ave", "lats": [35.052, 35.052], "lngs": [-97.970, -97.910]},
    {"name": "Choctaw Ave", "lats": [35.055, 35.055], "lngs": [-97.970, -97.910]},
    {"name": "4th St (Hwy 81)", "lats": [35.015, 35.075], "lngs": [-97.938, -97.938]},
    {"name": "16th St", "lats": [35.015, 35.075], "lngs": [-97.952, -97.952]},
    {"name": "29th St", "lats": [35.015, 35.075], "lngs": [-97.965, -97.965]}
]

fig, ax = plt.subplots(figsize=(14, 12), facecolor='#1a1a1a')
ax.set_facecolor('#1a1a1a')

# 1. Create the Heatmap Gradient Background
gradient = np.zeros((100, 100))
for i in range(100):
    gradient[i, :] = i / 99.0 
ax.imshow(gradient, extent=[lngs_range[0], lngs_range[1], lats_range[0], lats_range[1]], 
          cmap='RdYlGn', alpha=0.4, origin='upper', aspect='auto')

# 2. Draw the "Street" Grid
for road in roads:
    ax.plot(road['lngs'], road['lats'], color='white', alpha=0.6, linewidth=2, zorder=2)
    # Label roads
    if road['name'] == "Grand Ave":
        ax.text(-97.915, 35.0525, road['name'], color='white', fontsize=10, fontweight='bold', alpha=0.8)
    elif road['name'] == "4th St (Hwy 81)":
        ax.text(-97.937, 35.072, road['name'], color='white', fontsize=10, rotation=90, fontweight='bold', alpha=0.8)

# 3. Plot the Properties with Pins
for p in properties:
    # Pin Shadow
    ax.scatter(p['lng'], p['lat'], color='black', s=300, alpha=0.5, zorder=4)
    # Pin
    ax.scatter(p['lng'], p['lat'], color=p['color'], s=250, edgecolors='white', linewidth=2, zorder=5)
    # Label with box
    ax.text(p['lng']+0.0015, p['lat'], p['name'], color='white', fontsize=11, fontweight='bold',
            bbox=dict(facecolor='black', alpha=0.6, edgecolor='none', boxstyle='round,pad=0.3'), zorder=6)

# 4. Final Polish
ax.set_title("BRASH TACTICAL OVERLAY - CHICKASHA, OK (73018)", color='white', fontsize=20, fontweight='bold', pad=20)
ax.set_xlim(lngs_range)
ax.set_ylim(lats_range)
ax.tick_params(colors='white')

# Legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label='Prime (South)', markerfacecolor='green', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='Transitional', markerfacecolor='yellow', markersize=12),
    Line2D([0], [0], marker='o', color='w', label='High Risk (North)', markerfacecolor='red', markersize=12)
]
ax.legend(handles=legend_elements, loc='upper right', facecolor='black', edgecolor='white', labelcolor='white')

plt.savefig('/home/clawdbot/.openclaw/workspace/chickasha_brash_overlay_v2.png', dpi=300, bbox_inches='tight')
print("Advanced overlay rendered.")
