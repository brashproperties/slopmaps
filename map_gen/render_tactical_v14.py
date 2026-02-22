
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
    {"name": "728 S 17TH ST", "lat": 35.0452, "lng": -97.9545, "color": (0, 255, 255)},
    {"name": "1219 W COLORADO", "lat": 35.0485, "lng": -97.9485, "color": (0, 165, 255)},
    {"name": "925 S 3RD ST", "lat": 35.0414, "lng": -97.9349, "color": (0, 69, 255)} 
]

# Landmarks
landmarks = [
    {"name": "USAO UNIVERSITY", "lat": 35.0350, "lng": -97.9480, "color": (255, 120, 0)},
    {"name": "DOG FOOD PLANT", "lat": 35.0612, "lng": -97.9468, "color": (0, 0, 139)},
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
m.add_marker(CircleMarker((map_center_lng, map_center_lat), 'white', 1))
pil_img = m.render().convert('RGB')
img = np.array(pil_img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

# HEATMAP LAYER (CV2) - RECALIBRATED WITH SURGICAL SOUTH-SIDE POCKETS
grid_res = 180
top_lat, bottom_lat = 35.068, 35.022
left_lng, right_lng = -97.975, -97.915

# (lat, lng, strength, r, g, b)
pockets = [
    # Danger Zones (Red)
    {"lat": 35.0415, "lng": -97.9343, "s": 0.012, "r": 255, "g": 0, "b": 0}, # 3rd St Core
    {"lat": 35.0612, "lng": -97.9468, "s": 0.015, "r": 255, "g": 0, "b": 0}, # Dog Food Plant
    {"lat": 35.0480, "lng": -97.9300, "s": 0.010, "r": 255, "g": 0, "b": 0}, # East Side Tracks
    {"lat": 35.0400, "lng": -97.9250, "s": 0.014, "r": 255, "g": 0, "b": 0}, # SE Distress (S of Grand)
    
    # Elite Anchors (Green)
    {"lat": 35.0340, "lng": -97.9580, "s": 0.020, "r": 0, "g": 255, "b": 0}, # S.West Elite
    {"lat": 35.0460, "lng": -97.9250, "s": 0.010, "r": 0, "g": 255, "b": 0}, # Marlin Ct
    
    # Stability (Blue)
    {"lat": 35.0350, "lng": -97.9480, "s": 0.010, "r": 0, "g": 0, "b": 255}, # USAO
]

heatmap_small = np.zeros((grid_res, grid_res, 3), dtype=np.uint8)
for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # 1. Start with Yellow baseline (BGR: 0, 255, 255)
        # We use a 0.5-weight yellow to allow blending
        red_sum, green_sum, blue_sum, weight_sum = 255*0.5, 255*0.5, 0, 0.5
        
        for p in pockets:
            dist = math.sqrt((cur_lat - p['lat'])**2 + (cur_lng - p['lng'])**2)
            if dist < p['s']:
                inf = (1 - (dist / p['s'])) ** 1.2 # Sharpened influence
                red_sum += p['r'] * inf
                green_sum += p['g'] * inf
                blue_sum += p['b'] * inf
                weight_sum += inf

        heatmap_small[r, c] = [int(blue_sum/weight_sum), int(green_sum/weight_sum), int(red_sum/weight_sum)]

heatmap_full = cv2.resize(heatmap_small, (width, height), interpolation=cv2.INTER_LINEAR)
cv2.addWeighted(heatmap_full, 0.35, img, 0.65, 0, img)

# UI DRAWING
def draw_precision_pin(img, x, y, color, label):
    pts = np.array([[x, y], [x-22, y-55], [x+22, y-55]], np.int32)
    cv2.fillPoly(img, [pts], color)
    cv2.circle(img, (x, y-55), 22, color, -1)
    cv2.circle(img, (x, y-55), 22, (255, 255, 255), 3)
    cv2.circle(img, (x, y-55), 7, (255, 255, 255), -1)
    
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 1.3
    thickness = 2
    (tw, th), bl = cv2.getTextSize(label, font, font_scale, thickness)
    bx, by = x + 35, y - 80
    cv2.rectangle(img, (bx, by), (bx + tw + 20, by + th + 20), (0, 0, 0), -1)
    cv2.rectangle(img, (bx, by), (bx + tw + 20, by + th + 20), (255, 255, 255), 2)
    cv2.putText(img, label, (bx + 10, by + th + 10), font, font_scale, (255, 255, 255), thickness)

for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_precision_pin(img, px, py, p['color'], p['name'])
for lm in landmarks:
    px, py = lonlat_to_pixel(lm['lng'], lm['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_precision_pin(img, px, py, lm['color'], f"LM: {lm['name']}")
for r in roads:
    px, py = lonlat_to_pixel(r['lng'], r['lat'], zoom, width, height, map_center_lng, map_center_lat)
    cv2.putText(img, r['name'], (px-100, py), cv2.FONT_HERSHEY_TRIPLEX, 1.6, (0, 255, 255), 3)

# MASTER HUD
cv2.rectangle(img, (50, 50), (950, 540), (0,0,0), -1)
cv2.rectangle(img, (50, 50), (950, 540), (255,255,255), 4)
cv2.putText(img, "BRASH COMMAND: V14 (POCKET CALIBRATED)", (80, 110), cv2.FONT_HERSHEY_DUPLEX, 1.9, (255,255,255), 3)
cv2.line(img, (80, 140), (920, 140), (255,255,255), 2)

legend = [
    ((0, 255, 0), "ELITE: S.WEST / MARLIN CT (GREEN)"),
    ((0, 255, 255), "CORE GROWTH: TRANSITIONAL (YELLOW)"),
    ((255, 120, 0), "STABILITY: USAO BLUE ZONE"),
    ((0, 165, 255), "SPECULATIVE: REHAB-HEAVY (ORANGE)"),
    ((0, 0, 255), "RISK: 3RD ST / INDUSTRIAL / SE POCKET (RED)")
]
y_l = 200
for color, text in legend:
    cv2.rectangle(img, (80, y_l), (120, y_l+30), color, -1)
    cv2.rectangle(img, (80, y_l), (120, y_l+30), (255,255,255), 1)
    cv2.putText(img, text, (140, y_l+25), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
    y_l += 65

cv2.imwrite('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v14_pockets.png', img)
print("V14 Pockets Map Rendered.")
