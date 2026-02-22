#!/usr/bin/env python3
"""
Fetch property comps data from PropertyReach API for Chickasha, OK
Using expanded seed list for maximum coverage
"""
import requests
import json
import time

API_KEY = "live_u9JyD3Hmp58wmEQEnyZ5GosDjDcXHH5SuUN"
ENDPOINT = "https://api.propertyreach.com/v1/comparables"

# Expanded seed addresses
SEED_ADDRESSES = [
    "925 S 3rd St",
    "201 W Washington Ave", 
    "920 S 7th St",
    "1015 S 8th St",
    "915 S 12th St",
    "920 S 17th St",
    "1922 S 21st St",
    "1225 S 8th St",
    "1001 S 17th St",
    "1001 W Minnesota Ave",
    "1002 S 5th St",
    "1005 S 5th St",
    "1014 S 8th St",
    "1016 S 4th St",
    "1025 S 5th St",
    "1028 S 16th St",
    "1101 W Minnesota Ave",
    "1113 W Texas Ave",
    "1119 S 5th St",
    "1123 W Missouri Ave",
    "1124 S 19th St",
    "1201 W Missouri Ave",
    "1207 W Missouri Ave",
    "1215 W Missouri Ave",
    "1216 S 12th St",
    "1220 S 12th St",
    "1227 W Missouri Ave",
    "1228 W Florida Ave",
    "1302 S 16th St",
    "1309 S 6th St",
    "1310 W Minnesota Ave",
    "1312 S 10th St",
    "1318 S 16th St",
    "1320 W Minnesota Ave",
    "1325 S 6th St",
    "1401 W Iowa Ave",
    "1402 S 14th St",
    "1408 S 8th St",
    "1414 S 11th St",
]

OUTPUT_FILE = "/home/clawdbot/projects/brash-maps/api/real_property_data.json"

def query_property_api(street_address):
    """Query the PropertyReach API for comps"""
    url = ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    payload = {
        "target": {
            "streetAddress": street_address,
            "city": "chickasha",
            "state": "ok"
        }
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        elif resp.status_code == 404:
            return {"error": "not_found", "message": "Subject property not found"}
        else:
            return {"error": f"status_{resp.status_code}", "message": resp.text[:200]}
    except Exception as e:
        return {"error": "exception", "message": str(e)}

def extract_all_comps(data):
    """Extract ALL comparable properties from API response"""
    properties = []
    
    if "error" in data:
        return properties
    
    if "meta" in data and data["meta"].get("status") != 200:
        return properties
    
    try:
        props = data.get("properties", [])
        
        seen = set()
        
        for prop in props:
            addr = prop.get("streetAddress", "")
            if addr and addr not in seen:
                seen.add(addr)
                properties.append({
                    "target_address": f"{addr}, chickasha, ok",
                    "lat": prop.get("latitude"),
                    "lon": prop.get("longitude"),
                    "estimated_value": prop.get("estimatedValue"),
                    "sale_price": prop.get("lastSaleAmount"),
                    "square_footage": prop.get("squareFeet"),
                    "vacancy_indicator": prop.get("vacant"),
                    "property_type": prop.get("propertyType"),
                    "land_use": prop.get("landUse"),
                    "year_built": prop.get("yearBuilt"),
                    "bedrooms": prop.get("bedrooms"),
                    "bathrooms": prop.get("bathrooms"),
                    "lots_sqft": prop.get("lotSquareFeet"),
                    "last_sale_date": prop.get("lastSaleDate"),
                    "comparable_source": prop.get("comparableSource"),
                    "distance_from_subject": prop.get("distanceFromSubject"),
                })
                
    except Exception as e:
        print(f"  Parse error: {e}")
    
    return properties

def main():
    print(f"Fetching property comps for Chickasha, OK...")
    print(f"Using {len(SEED_ADDRESSES)} seed addresses to extract comps\n")
    
    all_properties = []
    seen_addresses = set()
    
    for i, addr in enumerate(SEED_ADDRESSES):
        print(f"Query {i+1}/{len(SEED_ADDRESSES)}: {addr}...", end=" ")
        
        data = query_property_api(addr)
        comps = extract_all_comps(data)
        
        new_count = 0
        for comp in comps:
            key = comp.get("target_address", "").lower()
            if key and key not in seen_addresses:
                seen_addresses.add(key)
                all_properties.append(comp)
                new_count += 1
        
        print(f"found {len(comps)} comps ({new_count} new)")
        
        # Rate limiting
        time.sleep(0.25)
    
    # Summary stats
    valid_values = [p for p in all_properties if p.get("estimated_value") is not None]
    valid_sale_prices = [p for p in all_properties if p.get("sale_price") is not None]
    valid_sqft = [p for p in all_properties if p.get("square_footage") is not None]
    valid_vacancy = [p for p in all_properties if p.get("vacancy_indicator") is not None]
    valid_coords = [p for p in all_properties if p.get("lat") is not None and p.get("lon") is not None]
    
    summary = {
        "total_properties_collected": len(all_properties),
        "with_estimated_value": len(valid_values),
        "with_sale_price": len(valid_sale_prices),
        "with_square_footage": len(valid_sqft),
        "with_vacancy": len(valid_vacancy),
        "with_coordinates": len(valid_coords),
        "city": "Chickasha, OK",
        "grid_bounds": {
            "lat_min": 35.01,
            "lat_max": 35.09,
            "lon_min": -97.98,
            "lon_max": -97.90
        }
    }
    
    # Save output
    output = {
        "summary": summary,
        "properties": all_properties
    }
    
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"DONE! Results saved to {OUTPUT_FILE}")
    print(f"{'='*60}")
    print(f"Total unique properties: {summary['total_properties_collected']}")
    print(f"With estimated value: {summary['with_estimated_value']}")
    print(f"With sale price: {summary['with_sale_price']}")
    print(f"With square footage: {summary['with_square_footage']}")
    print(f"With vacancy data: {summary['with_vacancy']}")
    print(f"With coordinates: {summary['with_coordinates']}")
    
    # Calculate some stats
    if valid_values:
        values = [p['estimated_value'] for p in valid_values]
        sqft_vals = [p['square_footage'] for p in valid_sqft]
        
        print(f"\nValue Stats:")
        print(f"  Min: ${min(values):,}")
        print(f"  Max: ${max(values):,}")
        print(f"  Avg: ${sum(values)//len(values):,}")
        
        if sqft_vals:
            print(f"\nSquare Footage Stats:")
            print(f"  Min: {min(sqft_vals):,}")
            print(f"  Max: {max(sqft_vals):,}")
            print(f"  Avg: {sum(sqft_vals)//len(sqft_vals):,}")
        
        vacant_count = sum(1 for p in valid_vacancy if p['vacancy_indicator'] == True)
        print(f"\nVacancy: {vacant_count} vacant out of {len(valid_vacancy)} ({100*vacant_count//len(valid_vacancy)}%)")

if __name__ == "__main__":
    main()
