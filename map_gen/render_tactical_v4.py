
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math

# Chickasha center
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

# Add invisible markers just to satisfy the staticmap engine's render requirements
for p in properties:
    m.add_marker(CircleMarker((p['lng'], p['lat']), p['color'], 1))

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

# Render base satellite
image = m.render()

# Create Heatmap Overlay - AGGRESSIVE CONTRAST
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

for y in range(height):
    ratio = y / height
    if ratio < 0.4: # North = Red to Yellow
        r, g, b = 255, int(255 * (ratio / 0.4)), 0
    elif ratio < 0.7: # Central = Yellow to Green
        r, g, b = int(255 * (1 - (ratio - 0.4) / 0.3)), 255, 0
    else: # South = Solid Green
        r, g, b = 0, 255, 0
    draw.line([(0, y), (width, y)], fill=(r, g, b, 80))

# Composite
combined = Image.alpha_composite(image.convert('RGBA'), overlay)
draw_final = ImageDraw.Draw(combined)

# Real-deal Pins
def draw_drop_pin(draw, x, y, color, label):
    # Shadow
    draw.ellipse([x-12, y-8, x+12, y+8], fill=(0,0,0,100))
    # Pin Body
    pin_pts = [(x, y), (x-15, y-35), (x+15, y-35)]
    draw.polygon(pin_pts, fill=color, outline='white')
    draw.ellipse([x-15, y-50, x+15, y-20], fill=color, outline='white')
    draw.ellipse([x-5, y-40, x+5, y-30], fill='white')
    # Label Box
    draw.rectangle([x+20, y-50, x+180, y-15], fill=(0,0,0,220), outline='white')
    draw.text((x+28, y-42), label, fill='white')

# Add 'em
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_drop_pin(draw_final, px, py, p['color'], p['name'])

# Master Legend
draw_final.rectangle([30, height-160, 320, height-30], fill=(0,0,0,240), outline='white')
draw_final.text((50, height-150), "BRASH PROPERTIES TACTICAL", fill='white')
draw_final.ellipse([50, height-115, 65, height-100], fill='#00FF00', outline='white')
draw_final.text((75, height-112), "GREEN: Prime Equity (South)", fill='#00FF00')
draw_final.ellipse([50, height-85, 65, height-70], fill='#FFFF00', outline='white')
draw_final.text((75, height-82), "YELLOW: Transitional (Central)", fill='#FFFF00')
draw_final.ellipse([50, height-55, 65, height-40], fill='#FF0000', outline='white')
draw_final.text((75, height-52), "RED: High Risk (North)", fill='#FF0000')

combined.save('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v4.png')
print("Tactical V4 Rendered.")
