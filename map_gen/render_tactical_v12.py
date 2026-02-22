
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
import cv2

# Chickasha center
map_center_lng, map_center_lat = -97.940, 35.045
zoom = 15
width, height = 2400, 2200 

# High-Res Satellite
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Properties
properties = [
    {"name": "1922 S 21ST ST", "lat": 35.0345, "lng": -97.9575, "color": (0, 255, 0)},
    {"name": "728 S 17TH ST", "lat": 35.0452, "lng": -97.9545, "color": (255, 255, 0)},
    {"name": "1219 W COLORADO", "lat": 35.0485, "lng": -97.9485, "color": (255, 165, 0)},
    {"name": "925 S 3RD ST", "lat": 35.0414, "lng": -97.9349, "color": (255, 69, 0)} 
]

# Landmarks
landmarks = [
    {"name": "USAO UNIVERSITY", "lat": 35.0350, "lng": -97.9480, "color": (0, 0, 255)},
    {"name": "DOG FOOD PLANT", "lat": 35.0612, "lng": -97.9468, "color": (139, 0, 0)},
    {"name": "MARLIN CT", "lat": 35.0460, "lng": -97.9250, "color": (0, 255, 0)}
]

# Main Roads
roads = [
    {"name": "GRAND AVE", "lat": 35.0510, "lng": -97.9420},
    {"name": "HWY 81 (4TH ST)", "lat": 35.0400, "lng": -97.9380},
    {"name": "16TH ST", "lat": 35.0400, "lng": -97.9525},
    {"name": "29TH ST", "lat": 35.0400, "lng": -97.9710}
]

# Projection
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

# Render base satellite
# dummy marker for staticmap
m.add_marker(CircleMarker((map_center_lng, map_center_lat), 'white', 1))
pil_img = m.render().convert('RGB')
# Convert to OpenCV (BGR)
img = np.array(pil_img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# HEATMAP LAYER (CV2)
overlay = img.copy()
grid_res = 150
top_lat, bottom_lat = 35.068, 35.022
left_lng, right_lng = -97.975, -97.915

danger_pockets = [
    {"lat": 35.0415, "lng": -97.9343, "strength": 0.012, "weight": 1.0}, 
    {"lat": 35.0612, "lng": -97.9468, "strength": 0.015, "weight": 1.0}, 
]
safe_anchors = [
    {"lat": 35.0340, "lng": -97.9580, "strength": 0.020, "weight": 1.0}, 
]

# Generate Heatmap Matrix
heatmap_small = np.zeros((grid_res, grid_res, 3), dtype=np.uint8)
for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # Baseline
        lat_ratio = (cur_lat - bottom_lat) / (top_lat - bottom_lat)
        b, g, r_v = 0, 255, 255 # Yellow baseline (BGR)
        if lat_ratio > 0.6: g = int(255 * (1 - (lat_ratio - 0.6) / 0.4))
        elif lat_ratio < 0.4: r_v = int(255 * (lat_ratio / 0.4))
            
        for dp in danger_pockets:
            dist = math.sqrt((cur_lat - dp['lat'])**2 + (cur_lng - dp['lng'])**2)
            if dist < dp['strength']:
                inf = (1 - (dist / dp['strength'])) * dp['weight']
                r_v, g = int(r_v * (1-inf) + 255 * inf), int(g * (1-inf))
        
        for sa in safe_anchors:
            dist = math.sqrt((cur_lat - sa['lat'])**2 + (cur_lng - sa['lng'])**2)
            if dist < sa['strength']:
                inf = (1 - (dist / sa['strength'])) * sa['weight']
                g, r_v = int(g * (1-inf) + 255 * inf), int(r_v * (1-inf))
        
        heatmap_small[r, c] = [b, g, r_v]

heatmap_full = cv2.resize(heatmap_small, (width, height), interpolation=cv2.INTER_LINEAR)
cv2.addWeighted(heatmap_full, 0.25, img, 0.75, 0, img)

# UI DRAWING (CV2 - VECTOR SHARP)
def draw_precision_pin(img, x, y, color, label):
    # Pin Drop
    pts = np.array([[x, y], [x-20, y-50], [x+20, y-50]], np.int32)
    cv2.fillPoly(img, [pts], color)
    cv2.circle(img, (x, y-50), 20, color, -1)
    cv2.circle(img, (x, y-50), 20, (255, 255, 255), 3) # Outline
    cv2.circle(img, (x, y-50), 6, (255, 255, 255), -1) # Hole
    
    # Label Box
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.2
    thickness = 2
    (tw, th), baseline = cv2.getTextSize(label, font, font_scale, thickness)
    
    # Background Box
    bx, by = x + 30, y - 70
    cv2.rectangle(img, (bx, by), (bx + tw + 20, by + th + 20), (0, 0, 0), -1)
    cv2.rectangle(img, (bx, by), (bx + tw + 20, by + th + 20), (255, 255, 255), 2)
    cv2.putText(img, label, (bx + 10, by + th + 10), font, font_scale, (255, 255, 255), thickness)

# Render Assets
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_precision_pin(img, px, py, p['color'], p['name'])

for lm in landmarks:
    px, py = lonlat_to_pixel(lm['lng'], lm['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_precision_pin(img, px, py, lm['color'], f"LM: {lm['name']}")

for r in roads:
    px, py = lonlat_to_pixel(r['lng'], r['lat'], zoom, width, height, map_center_lng, map_center_lat)
    cv2.putText(img, r['name'], (px-100, py), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 255, 255), 3)

# MASTER HUD
cv2.rectangle(img, (50, 50), (850, 480), (0,0,0), -1)
cv2.rectangle(img, (50, 50), (850, 480), (255,255,255), 4)
cv2.putText(img, "BRASH COMMAND: CHICKASHA V12", (80, 110), cv2.FONT_HERSHEY_DUPLEX, 1.8, (255,255,255), 3)
cv2.line(img, (80, 140), (820, 140), (255,255,255), 2)

legend = [
    ((0, 255, 0), "ELITE: S.WEST ALPHA"),
    ((0, 255, 255), "CORE GROWTH: TRANSITIONAL"),
    ((0, 165, 255), "SPECULATIVE: REHAB-HEAVY"),
    ((0, 69, 255), "HIGH YIELD: 3RD ST CORE"),
    ((0, 0, 139), "RISK: INDUSTRIAL NORTH")
]

y_l = 200
for color, text in legend:
    cv2.rectangle(img, (80, y_l), (120, y_l+30), color, -1)
    cv2.rectangle(img, (80, y_l), (120, y_l+30), (255,255,255), 1)
    cv2.putText(img, text, (140, y_l+25), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
    y_l += 55

cv2.imwrite('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v12_vector.png', img)
print("V12 Vector-Sharp Map Rendered.")
