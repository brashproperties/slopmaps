
from staticmap import StaticMap, CircleMarker
from PIL import Image, ImageDraw, ImageFont
import math
import numpy as np
import cv2

# Evansville / Vanderburgh center
map_center_lng, map_center_lat = -87.58, 37.97
zoom = 13
width, height = 2400, 2200 

# High-Res Satellite
m = StaticMap(width, height, url_template='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}')

# Portfolio Properties
properties = [
    {"name": "1320 N FARES AVE", "lat": 38.0015, "lng": -87.5845, "color": (0, 0, 255)}, # Blue - High Yield
    {"name": "721 SMITH RD", "lat": 37.9320, "lng": -87.8980, "color": (0, 165, 255)}, # Orange - Speculative
    {"name": "923 W OREGON ST", "lat": 37.9645, "lng": -87.5990, "color": (0, 0, 255)}, # Blue - High Yield
]

# Landmarks
landmarks = [
    {"name": "UNIVERSITY OF EVANSVILLE", "lat": 37.9750, "lng": -87.5600, "color": (0, 255, 0)}, # Green - Elite
    {"name": "MEDICAL DISTRICT", "lat": 37.9900, "lng": -87.5700, "color": (255, 120, 0)}, # Blue - Stability
    {"name": "TOYOTA PLANT (PRINCETON)", "lat": 38.3500, "lng": -87.5800, "color": (255, 0, 0)}, # Red - Economic Anchor
]

# Main Roads
roads = [
    {"name": "LLOYD EXPWY", "lat": 37.9700, "lng": -87.6200},
    {"name": "DIAMOND AVE", "lat": 37.9700, "lng": -87.5500},
    {"name": "GREEN RIVER RD", "lat": 37.9800, "lng": -87.5800},
    {"name": "US 41", "lat": 37.9500, "lng": -87.5700},
]

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

# HEATMAP LAYER - Vanderburgh Zones
grid_res = 150
top_lat, bottom_lat = 38.050, 37.900
left_lng, right_lng = -87.750, -87.450

# Zone Anchors (lng, lat, strength, r, g, b)
zones = [
    # Elite - University District
    {"lat": 37.9750, "lng": -87.5600, "s": 0.015, "r": 0, "g": 255, "b": 0},
    # Core Growth - Westside / Riverside
    {"lat": 37.9650, "lng": -87.6300, "s": 0.020, "r": 255, "g": 255, "b": 0},
    # Stability - Downtown / Medical
    {"lat": 37.9850, "lng": -87.5700, "s": 0.012, "r": 255, "g": 120, "b": 0},
    # Speculative - Eastside
    {"lat": 37.9600, "lng": -87.5300, "s": 0.018, "r": 255, "g": 165, "b": 0},
    # High Yield - Northside / Diamond
    {"lat": 37.9800, "lng": -87.5450, "s": 0.015, "r": 255, "g": 0, "b": 0},
]

heatmap_small = np.zeros((grid_res, grid_res, 3), dtype=np.uint8)
for r in range(grid_res):
    for c in range(grid_res):
        cur_lat = top_lat - (r / grid_res) * (top_lat - bottom_lat)
        cur_lng = left_lng + (c / grid_res) * (right_lng - left_lng)
        
        # Start Yellow baseline
        red_sum, green_sum, blue_sum, weight_sum = 255*0.5, 255*0.5, 0, 0.5
        
        for z in zones:
            dist = math.sqrt((cur_lat - z['lat'])**2 + (cur_lng - z['lng'])**2)
            if dist < z['s']:
                inf = (1 - (dist / z['s'])) ** 1.2
                red_sum += z['r'] * inf
                green_sum += z['g'] * inf
                blue_sum += z['b'] * inf
                weight_sum += inf

        heatmap_small[r, c] = [int(blue_sum/weight_sum), int(green_sum/weight_sum), int(red_sum/weight_sum)]

heatmap_full = cv2.resize(heatmap_small, (width, height), interpolation=cv2.INTER_LINEAR)
cv2.addWeighted(heatmap_full, 0.35, img, 0.65, 0, img)

def draw_pin(img, x, y, color, label):
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

# Render Properties
for p in properties:
    px, py = lonlat_to_pixel(p['lng'], p['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_pin(img, px, py, p['color'], p['name'])

# Render Landmarks
for lm in landmarks:
    px, py = lonlat_to_pixel(lm['lng'], lm['lat'], zoom, width, height, map_center_lng, map_center_lat)
    draw_pin(img, px, py, lm['color'], f"LM: {lm['name']}")

# Render Roads
for r in roads:
    px, py = lonlat_to_pixel(r['lng'], r['lat'], zoom, width, height, map_center_lng, map_center_lat)
    cv2.putText(img, r['name'], (px-100, py), cv2.FONT_HERSHEY_TRIPLEX, 1.6, (0, 255, 255), 3)

# HUD
cv2.rectangle(img, (50, 50), (950, 520), (0,0,0), -1)
cv2.rectangle(img, (50, 50), (950, 520), (255,255,255), 4)
cv2.putText(img, "BRASH COMMAND: VANDERBURGH COUNTY V1", (80, 110), cv2.FONT_HERSHEY_DUPLEX, 1.9, (255,255,255), 3)
cv2.line(img, (80, 140), (920, 140), (255,255,255), 2)

y_l = 200
legend = [
    ((0, 255, 0), "ELITE: UNIVERSITY DISTRICT"),
    ((0, 255, 255), "CORE GROWTH: WESTSIDE/RIVERSIDE"),
    ((255, 120, 0), "STABILITY: DOWNTOWN/MEDICAL"),
    ((0, 165, 255), "SPECULATIVE: EASTSIDE"),
    ((0, 0, 255), "HIGH YIELD: NORTHSIDE/DIAMOND")
]
for color, text in legend:
    cv2.rectangle(img, (80, y_l), (120, y_l+30), color, -1)
    cv2.rectangle(img, (80, y_l), (120, y_l+30), (255,255,255), 1)
    cv2.putText(img, text, (140, y_l+25), cv2.FONT_HERSHEY_DUPLEX, 1.1, (255,255,255), 2)
    y_l += 60

cv2.imwrite('/home/clawdbot/.openclaw/workspace/vanderburgh_tactical_v1.png', img)
print("Vanderburgh Map V1 Rendered.")
