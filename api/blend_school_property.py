#!/usr/bin/env python3
"""
Blend Chickasha school data with property values to create a new grid.
"""

import json
import math

# Load property data
with open('/home/clawdbot/projects/brash-maps/api/real_property_data.json', 'r') as f:
    data = json.load(f)

properties = data['properties']

# School ratings (from research)
SCHOOL_RATINGS = {
    'grand_ave_elementary': 8,    # Best - North of Chickasha Ave, between 19th and 9th St
    'lincoln_elementary': 6,       # Middle rating
    'chickasha_middle': 6,          # Middle rating
    'chickasha_high': 5             # Lowest rating
}

# Grid parameters (from original data bounds)
lat_min = 35.01
lat_max = 35.09
lon_min = -97.98
lon_max = -97.90
cell_size = 0.005  # ~500m cells

def get_school_zone(lat, lon):
    """
    Determine school zone based on location.
    Chickasha geography:
    - Higher lat = North
    - More negative lon = West
    - Street numbers increase going north
    - Chickasha Ave is around lat 35.045
    """
    # Define zones based on approximate boundaries
    # Grand Avenue Elementary: North of Chickasha Ave (~35.04), between 19th and 9th St
    if lat >= 35.035 and lon >= -97.96 and lon <= -97.93:
        return 'grand_ave_elementary'
    # Lincoln Elementary/Middle: West side of town
    elif lon < -97.94:
        return 'lincoln_elementary'
    # Chickasha Middle School: Central/south
    elif lat < 35.04:
        return 'chickasha_middle'
    # Chickasha High School: East/south area
    else:
        return 'chickasha_high'

def get_school_rating(school_zone):
    return SCHOOL_RATINGS.get(school_zone, 5)

# Calculate value per sqft for each property (using last sale price, which is closer to tax-assessed value)
for prop in properties:
    prop['value_per_sqft'] = prop.get('sale_price', 0) / prop['square_footage'] if prop['square_footage'] > 0 else 0
    prop['school_zone'] = get_school_zone(prop['lat'], prop['lon'])
    prop['school_rating'] = get_school_rating(prop['school_zone'])

# Get value/sqft range for normalization
value_per_sqft_values = [p['value_per_sqft'] for p in properties]
min_vpsf = min(value_per_sqft_values)
max_vpsf = max(value_per_sqft_values)

print(f"Value/sqft range: ${min_vpsf:.2f} - ${max_vpsf:.2f}")

# Normalize value/sqft to 0-1 scale
for prop in properties:
    if max_vpsf > min_vpsf:
        prop['vpsf_normalized'] = (prop['value_per_sqft'] - min_vpsf) / (max_vpsf - min_vpsf)
    else:
        prop['vpsf_normalized'] = 0.5
    
    # Normalize school rating to 0-1 (5-10 range -> 0-1)
    prop['school_normalized'] = (prop['school_rating'] - 5) / 5  # 5->0, 8->0.6
    
    # Calculate blended score (50% property value, 50% school quality)
    prop['blended_score'] = (prop['vpsf_normalized'] * 0.5) + (prop['school_normalized'] * 0.5)

# Show some examples
print("\nSample properties with scores:")
for prop in properties[:10]:
    print(f"  {prop['target_address'][:30]:30s} | VPSF: ${prop['value_per_sqft']:6.0f} | School: {prop['school_zone'][:20]:20s} ({prop['school_rating']}/10) | Blended: {prop['blended_score']:.3f}")

# Count properties by school zone
zone_counts = {}
for prop in properties:
    zone = prop['school_zone']
    zone_counts[zone] = zone_counts.get(zone, 0) + 1

print(f"\nProperties by school zone:")
for zone, count in zone_counts.items():
    print(f"  {zone}: {count}")

# Generate grid
grid_cells = []
grid_bounds = {
    'lat_min': lat_min,
    'lat_max': lat_max,
    'lon_min': lon_min,
    'lon_max': lon_max,
    'cell_size': cell_size
}

# Create grid cells
lat = lat_min
while lat < lat_max:
    lon = lon_min
    while lon < lon_max:
        cell_lat = lat + cell_size / 2
        cell_lon = lon + cell_size / 2
        
        # Find properties in this cell
        cell_properties = [
            p for p in properties
            if p['lat'] >= lat and p['lat'] < lat + cell_size
            and p['lon'] >= lon and p['lon'] < lon + cell_size
        ]
        
        if cell_properties:
            # Use average blended score of properties in cell
            avg_score = sum(p['blended_score'] for p in cell_properties) / len(cell_properties)
            cell_data = {
                'lat': cell_lat,
                'lon': cell_lon,
                'score': avg_score,
                'property_count': len(cell_properties),
                'has_properties': True,
                'sample_address': cell_properties[0]['target_address']
            }
        else:
            # Directional gradient for cells without properties
            # Southwest = better (better schools), Northeast = worse
            # Normalize position within grid
            lat_norm = (cell_lat - lat_min) / (lat_max - lat_min)
            lon_norm = (cell_lon - lon_min) / (lon_max - lon_min)
            
            # Combined gradient (southwest = low values = high score for "good")
            # Invert so southwest (high score) = better area
            gradient_score = 1 - ((lat_norm + lon_norm) / 2)
            # Scale to reasonable range (0.3-0.7 to match property scores)
            gradient_score = 0.3 + (gradient_score * 0.4)
            
            cell_data = {
                'lat': cell_lat,
                'lon': cell_lon,
                'score': gradient_score,
                'property_count': 0,
                'has_properties': False,
                'sample_address': None
            }
        
        grid_cells.append(cell_data)
        
        lon += cell_size
    lat += cell_size

# Summary stats
cells_with_properties = sum(1 for c in grid_cells if c['has_properties'])
cells_without_properties = sum(1 for c in grid_cells if not c['has_properties'])

print(f"\nGrid generated:")
print(f"  Total cells: {len(grid_cells)}")
print(f"  Cells with properties: {cells_with_properties}")
print(f"  Cells without properties: {cells_without_properties}")

# Score distribution
scores_with_prop = [c['score'] for c in grid_cells if c['has_properties']]
scores_without_prop = [c['score'] for c in grid_cells if not c['has_properties']]

print(f"\nScore ranges:")
if scores_with_prop:
    print(f"  With properties: {min(scores_with_prop):.3f} - {max(scores_with_prop):.3f}")
if scores_without_prop:
    print(f"  Without properties: {min(scores_without_prop):.3f} - {max(scores_without_prop):.3f}")

# Create output data structure
output = {
    'summary': {
        'total_properties': len(properties),
        'total_grid_cells': len(grid_cells),
        'cells_with_properties': cells_with_properties,
        'cells_without_properties': cells_without_properties,
        'grid_bounds': grid_bounds,
        'scoring_method': '50% value_per_sqft + 50% school_quality',
        'school_zones': SCHOOL_RATINGS
    },
    'properties': properties,
    'grid_cells': grid_cells
}

# Write output
output_path = '/home/clawdbot/projects/brash-maps/api/grid_data.json'
with open(output_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nOutput written to: {output_path}")
