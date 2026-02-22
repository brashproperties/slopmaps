
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np

# Chickasha center
map_center_lng, map_center_lat = -97.940, 35.045
zoom = 15
width, height = 2400, 2200 

# High-Res Satellite
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21st St", "lat": 35.0345, "lng": -97.9575, "color": "#00FF00"},
    {"name": "728 S 17th St", "lat": 35.0452, "lng": -97.9545, "color": "#FFFF00"},
    {"name": "1219 W Colorado", "lat": 35.0485, "lng": -97.9485, "color": "#FFA500"},
    {"name": "925 S 3rd St", "lat": 35.0414, "lng": -97.9349, "color": "#FF4500"} # Orange-Red
]

# Landmarks & Shift Points
landmarks = [
    {"name": "USAO University (Blue Zone)", "lat": 35.0350, "lng": -97.9480, "color": "#0000FF"},
    {"name": "Dog Food Plant", "lat": 35.0612, "lng": -97.9468, "color": "#8B0000"},
    {"name": "Marlin Ct (Hidden Green)", "lat": 35.0460, "lng": -97.9250, "color": "#00FF00"}
]

# Main Roads
roads = [
    {"name": "GRAND AVE", "lat": 35.0510, "lng": -97.9420},
    {"name": "HWY 81 (4th St)", "lat": 35.0400, "lng": -97.9380},
    {"name": "HWY 62 Corridor", "lat": 35.0510, "lng": -97.9250},
    {"name": "16th ST", "lat": 35.0400, "lng": -97.9525},
    {"name": "29th ST", "lat": 35.0400, "lng": -97.9710}
]

for p in properties + landmarks:
    m.add_marker(CircleMarker((p['lng'], p['lat']), p['color'], 1))

def lonlat_to_pixel(lon, lat, zoom, width, height, center_lon, center_lat):
    def lon_to_x(lon, zoom): return (lon + 180.0) / 360.0 * (2.0 ** zoom)
    def lat_to_y(lat, zoom):
        lat_rad = math.radians(lat)
        return (1.0 - math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi) / 2.0 * (2.0 ** zoom)
    center_x, center_y = lon_to_x(center_lon, zoom), lat_to_y(center_lat, zoom)
    target_x, target_y = lon_to_x(lon, zoom), lat_to_y(lat, zoom)
    pixel_x = (target_x - center_x) * 256 + width / 2
    pixel_y = (target_y - center_y) * 256 + height / 2
    return int(pixel_x), int(pixel_y)

image = m.render()

# V10 GATEWAY EDITION HEATMAP
overlay = Image.new('RGBA', image.size, (0,0,0,0))
grid_res = 180 
heatmap_data = np.zeros((grid_res, grid_res, 4))

# Updated Analyst Influence Points
danger_pockets = [
    {"lat": 35.0415, "lng": -97.9343, "strength": 0.008, "weight": 0.7}, # 3rd St (Softened)
    {"lat": 35.0612, "lng": -97.9468, "strength": 0.015, "weight": 1.0}, # Dog Food Plant
    {"lat": 35.0480, "lng": -97.9300, "strength": 0.010, "weight": 0.8}, # East Side Tracks
]
safe_anchors = [
    {"lat": 35.0340, "lng": -97.9580, "strength": 0.015, "weight": 1.0}, # S.West Elite
    {"lat": 35.0460, "lng": -97.9250, "strength": 0.010, "weight": 0.9}, # Marlin Ct Hidden Green
]
blue_zones = [
    {"lat": 35.0350, "lng": -97.9480, "strength": 0.010, "weight": 1.0}, # USAO Stability Zone
]
yellow_strips = [
    {"lat": 35.0510, "lng": -97.9250, "strength": 0.015, "weight": 0.8}, # Hwy 62 Corridor Upgrade
]

top_lat, bottom_lat = 35.068, 35.022
left_lng, right_lng = -97.975, -97.915

for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # 1. Base Gradient
        lat_ratio = (cur_lat - bottom_lat) / (top_lat - bottom_lat)
        r_val, g_val, b_val = 255, 255, 0 # Default Yellow
        if lat_ratio > 0.6: g_val = int(255 * (1 - (lat_ratio - 0.6) / 0.4))
        elif lat_ratio < 0.4: r_val = int(255 * (lat_ratio / 0.4))
            
        # 2. Danger (Red)
        for dp in danger_pockets:
            dist = math.sqrt((cur_lat - dp['lat'])**2 + (cur_lng - dp['lng'])**2)
            if dist < dp['strength']:
                inf = (1 - (dist / dp['strength'])) * dp['weight']
                r_val, g_val = int(r_val * (1-inf) + 255 * inf), int(g_val * (1-inf))
        
        # 3. Safe (Green)
        for sa in safe_anchors:
            dist = math.sqrt((cur_lat - sa['lat'])**2 + (cur_lng - sa['lng'])**2)
            if dist < sa['strength']:
                inf = (1 - (dist / sa['strength'])) * sa['weight']
                g_val, r_val = int(g_val * (1-inf) + 255 * inf), int(r_val * (1-inf))
        
        # 4. Blue Zone (Stability)
        b_val = 0
        for bz in blue_zones:
            dist = math.sqrt((cur_lat - bz['lat'])**2 + (cur_lng - bz['lng'])**2)
            if dist < bz['strength']:
                inf = (1 - (dist / bz['strength'])) * bz['weight']
                b_val = int(255 * inf)
                r_val, g_val = int(r_val * (1-inf)), int(g_val * (1-inf))

        heatmap_data[r, c] = [r_val, g_val, b_val, 80]

heatmap_img = Image.fromarray(heatmap_data.astype('uint8'), 'RGBA').resize((width, height), Image.Resampling.BILINEAR)
combined = Image.alpha_composite(image.convert('RGBA'), heatmap_img)
draw = ImageDraw.Draw(combined)

def draw_pin(draw, x, y, color, label, is_lm=False):
    draw.ellipse([x-20, y-12, x+20, y+12], fill=(0,0,0,100))
    pts = [(x, y), (x-25, y-50), (x+25, y-50)]
    draw.polygon(pts, fill=color, outline='white', width=2)
    draw.ellipse([x-25, y-75, x+25, y-40], fill=color, outline='white', width=2)
    draw.rectangle([x+30, y-75, x+320, y-30], fill=(0,0,0,230), outline='white', width=2)
    draw.text((x+40, y-60), f"{'LM: ' if is_lm else ''}{label}", fill='white')

for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_pin(draw, px, py, p['color'], p['name'])
for lm in landmarks:
    px, py = lonlat_to_pixel(lm['lng'], lm['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_pin(draw, px, py, lm['color'], lm['name'], is_lm=True)
for r in roads:
    px, py = lonlat_to_pixel(r['lng'], r['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw.rectangle([px-100, py-25, px+100, py+25], fill=(0,0,0,200), outline='white', width=2)
    draw.text((px-85, py-10), r['name'], fill='#FFFF00')

draw.rectangle([50, 50, 750, 420], fill=(0,0,0,250), outline='white', width=4)
draw.text((80, 70), "BRASH TACTICAL COMMAND - V10 (GATEWAY EDITION)", fill='white')
draw.line([80, 100, 720, 100], fill='white', width=2)
y = 120
legend = [
    ("#00FF00", "ELITE: S.West Alpha / Marlin Ct Hidden Green"),
    ("#FFFF00", "CORE GROWTH: Hwy 62 / Transitional"),
    ("#0000FF", "STABILITY: USAO University Blue Zone"),
    ("#FFA500", "SPECULATIVE: Rehab-Heavy / Core Boundary"),
    ("#FF4500", "HIGH YIELD: 3rd St Strip (Orange-Red)"),
    ("#FF0000", "CRITICAL RISK: Industrial North / Tracks")
]
for col, txt in legend:
    draw.ellipse([80, y, 105, y+25], fill=col, outline='white')
    draw.text((120, y+5), txt, fill='white')
    y += 40

combined.save('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v10_gateway.png')
print("V10 Rendered.")
