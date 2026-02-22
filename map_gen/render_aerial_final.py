
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math

# Chickasha center
map_center_lng, map_center_lat = -97.940, 35.045
zoom = 14
width, height = 1200, 1000

# Using Esri Satellite as the tile provider
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "green"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "yellow"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "orange"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "red"}
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

# Add markers for the staticmap engine
for p in properties:
    color_val = p['color']
    if color_val == 'orange': color_val = '#ffa500'
    marker = CircleMarker((p['lng'], p['lat']), color_val, 18)
    m.add_marker(marker)

# Render the base satellite map
image = m.render()

# Add a semi-transparent heatmap gradient overlay
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

for y in range(height):
    ratio = y / height
    if ratio < 0.5: # Red to Yellow
        r, g, b = 255, int(255 * (ratio * 2)), 0
    else: # Yellow to Green
        r, g, b = int(255 * (1 - (ratio - 0.5) * 2)), 255, 0
    draw.line([(0, y), (width, y)], fill=(r, g, b, 50))

# Composite the heatmap onto the satellite image
combined = Image.alpha_composite(image.convert('RGBA'), overlay)
draw_final = ImageDraw.Draw(combined)

# Add Labels using manual projection
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    
    # Draw label box and text
    label = p['name']
    draw_final.rectangle([px + 12, py - 12, px + 160, py + 12], fill=(0,0,0,200), outline='white')
    draw_final.text((px + 18, py - 8), label, fill='white')

# Add Legend
draw_final.rectangle([20, height - 120, 220, height - 20], fill=(0,0,0,220), outline='white')
draw_final.text((35, height - 110), "ZONE ANALYSIS", fill='white')
draw_final.ellipse([35, height-85, 45, height-75], fill='green', outline='white')
draw_final.text((55, height-85), "Prime (South)", fill='white')
draw_final.ellipse([35, height-65, 45, height-55], fill='yellow', outline='white')
draw_final.text((55, height-65), "Transitional", fill='white')
draw_final.ellipse([35, height-45, 45, height-35], fill='red', outline='white')
draw_final.text((55, height-45), "High Risk (North)", fill='white')

# Save
combined.save('/home/clawdbot/.openclaw/workspace/chickasha_brash_aerial_final.png')
print("Aerial tactical map generated successfully.")
