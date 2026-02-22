
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
    {"name": "1922 S 21ST ST", "lat": 35.0345, "lng": -97.9575, "color": (0, 255, 0)}, # Green
    {"name": "728 S 17TH ST", "lat": 35.0452, "lng": -97.9545, "color": (0, 255, 255)}, # Yellow
    {"name": "1219 W COLORADO", "lat": 35.0485, "lng": -97.9485, "color": (0, 165, 255)}, # Orange
    {"name": "925 S 3RD ST", "lat": 35.0414, "lng": -97.9349, "color": (0, 0, 255)} # Red
]

# Landmarks
landmarks = [
    {"name": "USAO UNIVERSITY", "lat": 35.0350, "lng": -97.9480, "color": (255, 120, 0)}, # Blue
    {"name": "DOG FOOD PLANT", "lat": 35.0612, "lng": -97.9468, "color": (0, 0, 139)}, # Dark Red
]

# Main Roads
roads = [
    {"name": "GRAND AVE", "lat": 35.0510, "lng": -97.9420},
    {"name": "HWY 81 (4TH ST)", "lat": 34.9927, "lng": -97.9380}, # Adjusted for better label placement
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

# HEATMAP LAYER (CV2) - RECALIBRATED GRADIENTS
grid_res = 150
top_lat, bottom_lat = 35.068, 35.022
left_lng, right_lng = -97.975, -97.915

# Specific Influence Points based on Analyst Audit
# (lat, lng, strength, weight_red, weight_green, weight_blue)
points = [
    {"lat": 35.0415, "lng": -97.9343, "s": 0.012, "r": 1.0, "g": 0.0, "b": 0.0}, # 3rd St Core (Hard Red)
    {"lat": 35.0612, "lng": -97.9468, "s": 0.015, "r": 1.0, "g": 0.0, "b": 0.0}, # Dog Food Plant (Hard Red)
    {"lat": 35.0340, "lng": -97.9580, "s": 0.020, "r": 0.0, "g": 1.0, "b": 0.0}, # S.West Elite (Hard Green)
    {"lat": 35.0350, "lng": -97.9480, "s": 0.010, "r": 0.0, "g": 0.0, "b": 1.0}, # USAO Stability (Hard Blue)
    {"lat": 35.0460, "lng": -97.9250, "s": 0.010, "r": 0.0, "g": 0.9, "b": 0.0}, # Marlin Ct (Hidden Green)
]

heatmap_small = np.zeros((grid_res, grid_res, 3), dtype=np.uint8)
for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # 1. Start with Yellow baseline (BGR: 0, 255, 255)
        blue_val, green_val, red_val = 0, 255, 255
        
        # 2. General Latitude Trend (North is Redder, South is Greener)
        lat_ratio = (cur_lat - bottom_lat) / (top_lat - bottom_lat) # 1 at north, 0 at south
        if lat_ratio > 0.6: # Northward transition to red
            green_val = int(255 * (1 - (lat_ratio - 0.6) / 0.4))
        elif lat_ratio < 0.4: # Southward transition to green
            red_val = int(255 * (lat_ratio / 0.4))
            
        # 3. Apply Local Influences
        for p in points:
            dist = math.sqrt((cur_lat - p['lat'])**2 + (cur_lng - p['lng'])**2)
            if dist < p['s']:
                inf = (1 - (dist / p['s']))
                # Blend colors
                red_val = int(red_val * (1-inf) + (255 if p['r'] > 0 else 0) * inf)
                green_val = int(green_val * (1-inf) + (255 if p['g'] > 0 else 0) * inf)
                blue_val = int(blue_val * (1-inf) + (255 if p['b'] > 0 else 0) * inf)

        heatmap_small[r, c] = [blue_val, green_val, red_val]

heatmap_full = cv2.resize(heatmap_small, (width, height), interpolation=cv2.INTER_LINEAR)
cv2.addWeighted(heatmap_full, 0.3, img, 0.7, 0, img)

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
cv2.rectangle(img, (50, 50), (900, 520), (0,0,0), -1)
cv2.rectangle(img, (50, 50), (900, 520), (255,255,255), 4)
cv2.putText(img, "BRASH COMMAND: V13 (CALIBRATED)", (80, 110), cv2.FONT_HERSHEY_DUPLEX, 1.9, (255,255,255), 3)
cv2.line(img, (80, 140), (870, 140), (255,255,255), 2)

legend = [
    ((0, 255, 0), "ELITE: S.WEST / MARLIN CT (GREEN)"),
    ((0, 255, 255), "CORE GROWTH: TRANSITIONAL (YELLOW)"),
    ((255, 120, 0), "STABILITY: USAO BLUE ZONE"),
    ((0, 165, 255), "SPECULATIVE: REHAB-HEAVY (ORANGE)"),
    ((0, 0, 255), "CRITICAL RISK: 3RD ST / INDUSTRIAL (RED)")
]
y_l = 200
for color, text in legend:
    cv2.rectangle(img, (80, y_l), (120, y_l+30), color, -1)
    cv2.rectangle(img, (80, y_l), (120, y_l+30), (255,255,255), 1)
    cv2.putText(img, text, (140, y_l+25), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
    y_l += 60

cv2.imwrite('/home/clawdbot/.openclaw/workspace/chickasha_tactical_v13_calibrated.png', img)
print("V13 Calibrated Map Rendered.")
