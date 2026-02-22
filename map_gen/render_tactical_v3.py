
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math

# Chickasha center - slightly adjusted for better coverage
map_center_lng, map_center_lat = -97.945, 35.045
zoom = 14
width, height = 1400, 1200

# Using Esri Satellite as the tile provider
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "#00FF00"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "#FFFF00"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "#FFA500"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "#FF0000"}
]

# Manual projection function (Web Mercator)
def lonlat_to_pixel(lon, lat, zoom, width, height, center_lon, center_lat):
    def lon_to_x(lon, zoom):
        return (lon + 180.0) / 360.0 * (2.0 ** zoom)
    def lat_to_y(lat, zoom):
        lat_rad = math.radians(lat)
        return (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * (2.0 ** zoom)

    center_x = lon_to_x(center_lon, zoom)
    center_y = lat_to_y(center_lat, zoom)
    target_x = lon_to_x(lon, zoom)
    target_y = lat_to_y(lat, zoom)
    
    pixel_x = (target_x - center_x) * 256 + width / 2
    pixel_y = (target_y - center_y) * 256 + height / 2
    return int(pixel_x), int(pixel_y)

# Render the base satellite map (no internal markers, we'll draw custom pins)
image = m.render()

# Create Heatmap Overlay - MORE AGGRESSIVE GRADIENT
# Row A-C (Top 30%) = Red
# Row D-F (Middle 30%) = Yellow
# Row G-J (Bottom 40%) = Green
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

for y in range(height):
    ratio = y / height
    if ratio < 0.4: # Top 40% (North) is Red transitioning to Yellow
        r = 255
        g = int(255 * (ratio / 0.4))
        b = 0
    elif ratio < 0.7: # Middle 30% is Yellow transitioning to Green
        r = int(255 * (1 - (ratio - 0.4) / 0.3))
        g = 255
        b = 0
    else: # Bottom 30% (South) is Deep Green
        r = 0
        g = 255
        b = 0
    
    # Draw horizontal line with slightly higher opacity for better visualization
    draw.line([(0, y), (width, y)], fill=(r, g, b, 75))

# Composite
combined = Image.alpha_composite(image.convert('RGBA'), overlay)
draw_final = ImageDraw.Draw(combined)

# Custom Pin Drawing Function
def draw_pin(draw, x, y, color, label):
    # Pin Drop Shape
    pin_points = [
        (x, y), 
        (x - 10, y - 25), 
        (x - 10, y - 35), 
        (x + 10, y - 35), 
        (x + 10, y - 25)
    ]
    draw.polygon(pin_points, fill=color, outline='white')
    draw.ellipse([x - 10, y - 45, x + 10, y - 25], fill=color, outline='white')
    draw.ellipse([x - 3, y - 38, x + 3, y - 32], fill='white') # Pin center hole
    
    # Label
    text_w = 140
    draw.rectangle([x + 15, y - 45, x + 15 + text_w, y - 15], fill=(0,0,0,220), outline='white')
    draw.text((x + 22, y - 38), label, fill='white')

# Add Pins
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_pin(draw_final, px, py, p['color'], p['name'])

# Legend
draw_final.rectangle([20, height - 150, 250, height - 20], fill=(0,0,0,230), outline='white')
draw_final.text((40, height - 140), "BRASH TACTICAL GRADES", fill='white')
draw_final.ellipse([40, height-110, 55, height-95], fill='#00FF00', outline='white')
draw_final.text((65, height-108), "Brash Green (Prime)", fill='white')
draw_final.ellipse([40, height-80, 55, height-65], fill='#FFFF00', outline='white')
draw_final.text((65, height-78), "Brash Yellow (Mid)", fill='white')
draw_final.ellipse([40, height-50, 55, height-35], fill='#FF0000', outline='white')
draw_final.text((65, height-48), "Brash Red (Risk)", fill='white')

# Save
combined.save('/home/clawdbot/.openclaw/workspace/chickasha_brash_tactical_v3.png')
print("Final Tactical Map Rendered.")
