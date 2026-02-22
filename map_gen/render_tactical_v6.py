
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

# Chickasha center - Sharp focus on the core residential area
map_center_lng, map_center_lat = -97.940, 35.045
zoom = 15 # Higher zoom for more detail
width, height = 2000, 1800 # Massive res for fidelity

# High-Res Satellite provider
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

# ULTRA-HIGH FIDELITY HEATMAP
# We're going to create a more complex gradient that isn't just vertical.
# We'll use radial influence points for the "Rough" pockets.
overlay = Image.new('RGBA', image.size, (0,0,0,0))
draw = ImageDraw.Draw(overlay)

# Geographic bounds of render (approximate at zoom 15)
# Using a 0.04 lat/lng spread
top_lat, bottom_lat = 35.060, 35.030
left_lng, right_lng = -97.970, -97.910

# Danger Pockets (North Core, East side near tracks, etc.)
danger_pockets = [
    {"lat": 35.055, "lng": -97.935, "strength": 0.015, "color": (255,0,0)}, # North/Downtown
    {"lat": 35.045, "lng": -97.930, "strength": 0.012, "color": (255,50,0)}, # East Central
]

# Prime Anchor (South West)
prime_anchors = [
    {"lat": 35.035, "lng": -97.960, "strength": 0.020, "color": (0,255,0)}
]

# Pixel-by-pixel color calc is too slow, we'll do a 50x50 matrix and upscale
grid_res = 100
heatmap_data = np.zeros((grid_res, grid_res, 4))

for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # Base color based on Latitude (North=Red, South=Green)
        lat_ratio = (cur_lat - bottom_lat) / (top_lat - bottom_lat) # 0 at bottom, 1 at top
        
        # Start with a baseline gradient
        if lat_ratio > 0.6: # North
            r_val, g_val, b_val = 255, int(255 * (1 - (lat_ratio-0.6)/0.4)), 0
        else: # South
            r_val, g_val, b_val = int(255 * (lat_ratio/0.6)), 255, 0
            
        # Distort based on pockets
        for p in danger_pockets:
            dist = math.sqrt((cur_lat - p['lat'])**2 + (cur_lng - p['lng'])**2)
            if dist < p['strength']:
                influence = 1 - (dist / p['strength'])
                r_val = int(r_val * (1-influence) + 255 * influence)
                g_val = int(g_val * (1-influence))
        
        heatmap_data[r, c] = [r_val, g_val, b_val, 70] # 70 opacity

# Upscale and apply
heatmap_img = Image.fromarray(heatmap_data.astype('uint8'), 'RGBA').resize((width, height), Image.Resampling.BILINEAR)
combined = Image.alpha_composite(image.convert('RGBA'), heatmap_img)
draw_final = ImageDraw.Draw(combined)

def draw_drop_pin(draw, x, y, color, label):
    # Shadow
    draw.ellipse([x-18, y-10, x+18, y+10], fill=(0,0,0,80))
    # Pin
    pin_pts = [(x, y), (x-20, y-45), (x+20, y-45)]
    draw.polygon(pin_pts, fill=color, outline='white')
    draw.ellipse([x-20, y-65, x+20, y-30], fill=color, outline='white')
    draw.ellipse([x-7, y-53, x+7, y-40], fill='white') # Center hole
    # Label with drop shadow
    draw.rectangle([x+25, y-65, x+240, y-20], fill=(0,0,0,220), outline='white', width=2)
    draw.text((x+35, y-53), label, fill='white', font=None)

# Render Pins at the new high res
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_drop_pin(draw_final, px, py, p['color'], p['name'])

# Professional HUD/Legend
hud_bg = (0,0,0,240)
draw_final.rectangle([40, 40, 500, 240], fill=hud_bg, outline='white', width=3)
draw_final.text((60, 60), "BRASH TACTICAL COMMAND - CHICKASHA", fill='white')
draw_final.line([60, 85, 480, 85], fill='white', width=1)

# Legend Items
y_off = 100
grades = [
    ("#00FF00", "ELITE: High Equity / South West"),
    ("#FFFF00", "TRANSITIONAL: Mid-Market Growth"),
    ("#FFA500", "SPECULATIVE: Rehab-Dependent"),
    ("#FF0000", "HIGH RISK: Core / North Distressed")
]

for color, text in grades:
    draw_final.ellipse([65, y_off, 85, y_off+20], fill=color, outline='white')
    draw_final.text((100, y_off+3), text, fill='white')
    y_off += 35

combined.save('/home/clawdbot/.openclaw/workspace/chickasha_brash_tactical_v6_hq.png')
print("High Fidelity V6 Rendered.")
