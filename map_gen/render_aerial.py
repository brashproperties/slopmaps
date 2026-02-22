
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import os

# Chickasha center
map_center = [-97.940, 35.045]
zoom = 14
width, height = 1200, 1000

# Using Esri Satellite as the tile provider
# URL: https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "green"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "yellow"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "orange"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "red"}
]

# Add markers
for p in properties:
    color_val = p['color']
    if color_val == 'orange': color_val = '#ffa500'
    marker = CircleMarker((p['lng'], p['lat']), color_val, 18)
    m.add_marker(marker)

# Render the base satellite map
image = m.render()

# Add a semi-transparent heatmap gradient overlay
# Since we want to show North=Red, South=Green, we'll create a vertical gradient
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

for y in range(height):
    # Map Y coordinate to a color: Top (y=0) is Red, Bottom (y=height) is Green
    # Red: (255, 0, 0), Yellow: (255, 255, 0), Green: (0, 255, 0)
    ratio = y / height
    if ratio < 0.5: # Red to Yellow
        r = 255
        g = int(255 * (ratio * 2))
        b = 0
    else: # Yellow to Green
        r = int(255 * (1 - (ratio - 0.5) * 2))
        g = 255
        b = 0
    
    # Draw a horizontal line with low opacity
    draw.line([(0, y), (width, y)], fill=(r, g, b, 60))

# Composite the heatmap onto the satellite image
combined = Image.alpha_composite(image.convert('RGBA'), overlay)

# Add Labels
draw_final = ImageDraw.Draw(combined)
try:
    # Try to load a font, fallback to default
    font = ImageFont.load_default()
except:
    font = None

for p in properties:
    # Convert lat/lng to pixel coordinates
    pixel_x, pixel_y = m.project((p['lng'], p['lat']))
    # Draw label box
    label = p['name']
    draw_final.rectangle([pixel_x + 10, pixel_y - 10, pixel_x + 150, pixel_y + 10], fill=(0,0,0,180))
    draw_final.text((pixel_x + 15, pixel_y - 7), label, fill='white', font=font)

# Add Title
draw_final.rectangle([width//2 - 250, 20, width//2 + 250, 70], fill=(0,0,0,200))
draw_final.text((width//2 - 200, 35), "BRASH TACTICAL AERIAL - CHICKASHA (73018)", fill='white', font=font)

# Save
combined.save('/home/clawdbot/.openclaw/workspace/chickasha_brash_aerial_v1.png')
print("Aerial map with heatmap overlay rendered successfully.")
