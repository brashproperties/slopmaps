#!/usr/bin/env python3
"""
Fetch property data from PropertyReach API for Chickasha, OK
Using search endpoint to get more properties with marketValue (tax assessor value)
"""
import requests
import json
import time

API_KEY = "live_u9JyD3Hmp58wmEQEnyZ5GosDjDcXHH5SuUN"
SEARCH_ENDPOINT = "https://api.propertyreach.com/v1/search"
PROPERTY_ENDPOINT = "https://api.propertyreach.com/v1/property"

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
    "1501 W Colorado Ave",
    "1505 S 9th St",
    "1510 S 4th St",
    "1601 W Chickasha Ave",
    "1605 S 6th St",
    "1610 S 2nd St",
    "1701 W Oklahoma Ave",
    "1708 S 5th St",
    "1715 S 3rd St",
    "1801 W Iowa Ave",
    "1805 S 7th St",
]

OUTPUT_FILE = "/home/clawdbot/projects/brash-maps/api/real_property_data.json"

def search_properties(city="chickasha", state="ok"):
    """Use search endpoint to get properties"""
    url = SEARCH_ENDPOINT
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    payload = {
        "target": {
            "city": city,
            "state": state.upper()
        },
        "filter": {},
        "limit": 200
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"status_{resp.status_code}", "message": resp.text[:200]}
    except Exception as e:
        return {"error": "exception", "message": str(e)}

def get_property_details(street_address, city, state):
    """Get detailed property info including marketValue"""
    url = PROPERTY_ENDPOINT
    headers = {
        "Content-Type": "application/json", 
        "X-API-Key": API_KEY
    }
    params = {
        "streetAddress": street_address,
        "city": city,
        "state": state.upper()
    }
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"status_{resp.status_code}"}
    except Exception as e:
        return {"error": "exception", "message": str(e)}

def extract_property_with_market_value(prop):
    """Extract property data including marketValue (tax assessor value)"""
    address = prop.get("streetAddress", "")
    
    # Get detailed property info to get marketValue
    details = get_property_details(address, "chickasha", "ok")
    
    market_value = None
    if details and "property" in details:
        prop_details = details["property"]
        # Try different field names for marketValue (tax assessor value)
        market_value = (
            prop_details.get("marketValue") or 
            prop_details.get("taxAssessedValue") or 
            prop_details.get("assessedValue") or
            prop_details.get("taxValue") or
            prop_details.get("taxAssessed") or
            prop_details.get("marketValue") or
            prop_details.get("assessedMarketValue")
        )
    
    # Calculate value_per_sqft from marketValue if available
    sqft = prop.get("squareFeet") or prop.get("livingSquareFeet") or 0
    if market_value and sqft and sqft > 0:
        value_per_sqft = market_value / sqft
    else:
        # Fall back to estimatedValue / sqft
        est_value = prop.get("estimatedValue", 0)
        if est_value and sqft and sqft > 0:
            value_per_sqft = est_value / sqft
        else:
            value_per_sqft = 0
    
    return {
        "target_address": f"{address}, chickasha, ok" if address else "",
        "lat": prop.get("latitude"),
        "lon": prop.get("longitude"),
        "estimated_value": prop.get("estimatedValue"),
        "market_value": market_value,
        "sale_price": prop.get("lastSaleAmount") or prop.get("lastSalePrice"),
        "square_footage": sqft,
        "vacancy_indicator": prop.get("vacant", False),
        "property_type": prop.get("propertyType"),
        "land_use": prop.get("landUse"),
        "year_built": prop.get("yearBuilt"),
        "bedrooms": prop.get("bedrooms"),
        "bathrooms": prop.get("bathrooms"),
        "lots_sqft": prop.get("lotSquareFeet") or prop.get("lotSizeSquareFeet"),
        "last_sale_date": prop.get("lastSaleDate"),
        "value_per_sqft": value_per_sqft,
        "comparable_source": prop.get("comparableSource"),
        "distance_from_subject": prop.get("distanceFromSubject"),
    }

def main():
    print(f"Fetching property data for Chickasha, OK...")
    print(f"Using search endpoint to get properties with marketValue\n")
    
    # First, search for all properties in Chickasha
    search_data = search_properties("chickasha", "ok")
    
    all_properties = []
    seen_addresses = set()
    
    if "error" in search_data:
        print(f"Search error: {search_data['error']}")
        print("Falling back to comps extraction method...")
        
        # Fall back to using comps from seed addresses
        pass
    else:
        # Extract properties from search results
        props = search_data.get("properties", [])
        print(f"Found {len(props)} properties in search results")
        
        for prop in props:
            addr = prop.get("streetAddress", "")
            if addr and addr.lower() not in seen_addresses:
                seen_addresses.add(addr.lower())
                
                # Get detailed info with marketValue
                prop_data = extract_property_with_market_value(prop)
                if prop_data.get("lat") and prop_data.get("lon"):
                    all_properties.append(prop_data)
                    print(f"  - {addr}: marketValue=${prop_data.get('market_value')}, value/sqft=${prop_data.get('value_per_sqft', 0):.2f}")
    
    # If we don't have enough properties, also use comps from seed addresses
    if len(all_properties) < 100:
        print(f"\nOnly got {len(all_properties)} properties from search, fetching comps from seed addresses...")
        
        # Import the comps extraction method from original script
        import sys
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Use the comps extraction for additional properties
        for addr in SEED_ADDRESSES[:20]:  # Limit to avoid too many API calls
            print(f"  Querying comps for: {addr}...")
            
            # Call comps endpoint
            url = "https://api.propertyreach.com/v1/comparables"
            headers = {
                "Content-Type": "application/json",
                "X-API-Key": API_KEY
            }
            payload = {
                "target": {
                    "streetAddress": addr,
                    "city": "chickasha",
                    "state": "ok"
                }
            }
            
            try:
                resp = requests.post(url, json=payload, headers=headers, timeout=30)
                if resp.status_code == 200:
                    comps_data = resp.json()
                    comps = comps_data.get("properties", [])
                    
                    for comp in comps:
                        caddr = comp.get("streetAddress", "")
                        if caddr and caddr.lower() not in seen_addresses:
                            seen_addresses.add(caddr.lower())
                            
                            # Get marketValue
                            prop_data = extract_property_with_market_value(comp)
                            if prop_data.get("lat") and prop_data.get("lon"):
                                all_properties.append(prop_data)
                                print(f"    + {caddr}: marketValue=${prop_data.get('market_value')}")
                
                time.sleep(0.3)
            except Exception as e:
                print(f"    Error: {e}")
    
    # Deduplicate by address
    unique_properties = []
    seen = set()
    for p in all_properties:
        addr = p.get("target_address", "").lower()
        if addr and addr not in seen:
            seen.add(addr)
            unique_properties.append(p)
    
    all_properties = unique_properties
    
    # Summary stats
    valid_market_value = [p for p in all_properties if p.get("market_value") is not None]
    valid_value_per_sqft = [p for p in all_properties if p.get("value_per_sqft") and p.get("value_per_sqft") > 0]
    valid_sqft = [p for p in all_properties if p.get("square_footage") and p.get("square_footage") > 0]
    valid_coords = [p for p in all_properties if p.get("lat") is not None and p.get("lon") is not None]
    
    summary = {
        "total_properties_collected": len(all_properties),
        "with_market_value": len(valid_market_value),
        "with_value_per_sqft": len(valid_value_per_sqft),
        "with_square_footage": len(valid_sqft),
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
    print(f"With marketValue: {summary['with_market_value']}")
    print(f"With value_per_sqft: {summary['with_value_per_sqft']}")
    print(f"With square footage: {summary['with_square_footage']}")
    print(f"With coordinates: {summary['with_coordinates']}")
    
    if valid_value_per_sqft:
        values = [p['value_per_sqft'] for p in valid_value_per_sqft]
        print(f"\nValue/sqft Stats:")
        print(f"  Min: ${min(values):.2f}")
        print(f"  Max: ${max(values):.2f}")
        print(f"  Avg: ${sum(values)/len(values):.2f}")

if __name__ == "__main__":
    import os
    main()
