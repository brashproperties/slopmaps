
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math

# Chickasha center - Shifted north to get 3rd st properly in frame
map_center_lng, map_center_lat = -97.940, 35.048
zoom = 14
width, height = 1400, 1400

# Using Esri Satellite
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "#00FF00"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "#FFFF00"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "#FFA500"},
    {"name": "925 S 3rd St", "lat": 35.0465, "lng": -97.9355, "color": "#FF0000"}
]

for p in properties:
    m.add_marker(CircleMarker((p['lng'], p['lat']), p['color'], 1))

def lonlat_to_pixel(lon, lat, zoom, width, height, center_lon, center_lat):
    def lon_to_x(lon, zoom):
        return (lon + 180.0) / 360.0 * (2.0 ** zoom)
    def lat_to_y(lat, zoom):
        lat_rad = math.radians(lat)
        return (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * (2.0 ** zoom)
    center_x, center_y = lon_to_x(center_lon, zoom), lat_to_y(center_lat, zoom)
    target_x, target_y = lon_to_x(lon, zoom), lat_to_y(lat, zoom)
    pixel_x = (target_x - center_x) * 256 + width / 2
    pixel_y = (target_y - center_y) * 256 + height / 2
    return int(pixel_x), int(pixel_y)

image = m.render()

# REALISTIC HEATMAP - FIXING THE GENEROSITY
# Grand Ave is roughly 35.052. Everything north of that is the danger zone.
# We need to map LATITUDE to the gradient, not just the image Y.
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

# Latitude bounds of our rendered image (approximate)
top_lat = 35.075
bottom_lat = 35.021

for y in range(height):
    # Calculate current latitude for this row
    current_lat = top_lat - (y / height) * (top_lat - bottom_lat)
    
    # NEW HARSH LOGIC:
    if current_lat > 35.055: # Deep North
        r, g, b, a = 255, 0, 0, 90 # Hard Red
    elif current_lat > 35.048: # North of Grand / Colorado area
        r, g, b, a = 255, 100, 0, 80 # Orange
    elif current_lat > 35.042: # Transitional / 17th St area
        r, g, b, a = 255, 255, 0, 60 # Yellow
    elif current_lat > 35.036: # Moving South
        r, g, b, a = 150, 255, 0, 50 # Lime
    else: # Deep South / 21st St area
        r, g, b, a = 0, 255, 0, 40 # Solid Green
        
    draw.line([(0, y), (width, y)], fill=(r, g, b, a))

combined = Image.alpha_composite(image.convert('RGBA'), overlay)
draw_final = ImageDraw.Draw(combined)

def draw_drop_pin(draw, x, y, color, label):
    draw.ellipse([x-12, y-8, x+12, y+8], fill=(0,0,0,100))
    pin_pts = [(x, y), (x-15, y-35), (x+15, y-35)]
    draw.polygon(pin_pts, fill=color, outline='white')
    draw.ellipse([x-15, y-50, x+15, y-20], fill=color, outline='white')
    draw.ellipse([x-5, y-40, x+5, y-30], fill='white')
    draw.rectangle([x+20, y-50, x+180, y-15], fill=(0,0,0,220), outline='white')
    draw.text((x+28, y-42), label, fill='white')

for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_drop_pin(draw_final, px, py, p['color'], p['name'])

# Master Legend
draw_final.rectangle([30, height-160, 350, height-30], fill=(0,0,0,240), outline='white')
draw_final.text((50, height-150), "BRASH PROPERTIES TACTICAL (HARSH)", fill='white')
draw_final.ellipse([50, height-115, 65, height-100], fill='#00FF00', outline='white')
draw_final.text((75, height-112), "GREEN: Prime Equity (Deep South)", fill='#00FF00')
draw_final.ellipse([50, height-85, 65, height-70], fill='#FFFF00', outline='white')
draw_final.text((75, height-82), "YELLOW: High Rental/Transitional", fill='#FFFF00')
draw_final.ellipse([50, height-55, 65, height-40], fill='#FF0000', outline='white')
draw_final.text((75, height-52), "RED: High Risk (Core/North)", fill='#FF0000')

combined.save('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v5_harsh.png')
print("Harsh Tactical V5 Rendered.")
