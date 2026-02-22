const fs = require('fs');

const propertyData = require('./api/real_property_data.json');

const GRID_SIZE = 0.005; // larger cells for smoother/fuzzier appearance
const LAT_MIN = 35.01;
const LAT_MAX = 35.09;
const LON_MIN = -97.98;
const LON_MAX = -97.90;

function getColorForPrice(pricePerSqft) {
    if (pricePerSqft === null || pricePerSqft === undefined) return 'transparent';
    
    const minPrice = -30;
    const maxPrice = 63;
    
    if (pricePerSqft < minPrice) return '#ff3300';
    if (pricePerSqft > maxPrice) return '#00cc00';
    
    const ratio = (pricePerSqft - minPrice) / (maxPrice - minPrice);
    
    if (ratio < 0.15) return '#ff3300';
    if (ratio < 0.3) return '#ff6600';
    if (ratio < 0.45) return '#ff9900';
    if (ratio < 0.6) return '#ffcc00';
    if (ratio < 0.75) return '#99cc00';
    if (ratio < 0.9) return '#66cc00';
    return '#00cc00';
}

function interpolateFromNearby(features, cellLat, cellLon, searchRadius = 0.02) {
    const nearbyWithData = features.filter(f => {
        if (!f.properties.has_real_data || f.properties.avg_sqft_price === null) return false;
        const dist = Math.sqrt(
            Math.pow(f.properties.center_lat - cellLat, 2) +
            Math.pow(f.properties.center_lon - cellLon, 2)
        );
        return dist < searchRadius && dist > 0;
    });
    
    if (nearbyWithData.length === 0) return null;
    
    const totalPrice = nearbyWithData.reduce((sum, f) => sum + f.properties.avg_sqft_price, 0);
    const avgPrice = Math.round(totalPrice / nearbyWithData.length);
    
    return avgPrice;
}

function calculateVibeScore(pricePerSqft) {
    if (pricePerSqft === null || pricePerSqft === undefined) return null;
    
    const minPrice = -30;
    const maxPrice = 63;
    
    const ratio = Math.max(0, Math.min(1, (pricePerSqft - minPrice) / (maxPrice - minPrice)));
    return 1 + (ratio * 9);
}

const features = [];

for (let lat = LAT_MIN; lat < LAT_MAX; lat += GRID_SIZE) {
    for (let lon = LON_MIN; lon < LON_MAX; lon += GRID_SIZE) {
        const cellLat = lat + GRID_SIZE / 2;
        const cellLon = lon + GRID_SIZE / 2;
        
        const nearbyProperties = propertyData.properties.filter(p => {
            return p.lat >= lat && p.lat < lat + GRID_SIZE &&
                   p.lon >= lon && p.lon < lon + GRID_SIZE;
        });
        
        let avgSqftPrice = null;
        let vibeScore = null;
        let propertyCount = 0;
        let color = 'transparent';
        let hasRealData = false;
        
        if (nearbyProperties.length > 0) {
            const validProperties = nearbyProperties.filter(p => 
                p.square_footage > 0 && p.market_value > 0
            );
            
            if (validProperties.length > 0) {
                const totalPricePerSqft = validProperties.reduce((sum, p) => {
                    return sum + (p.market_value / p.square_footage);
                }, 0);
                
                avgSqftPrice = Math.round(totalPricePerSqft / validProperties.length);
                vibeScore = Math.round(calculateVibeScore(avgSqftPrice) * 10) / 10;
                propertyCount = validProperties.length;
                color = getColorForPrice(avgSqftPrice);
                hasRealData = true;
            }
        }
        
        if (!hasRealData) {
            const interpolatedPrice = interpolateFromNearby(features, cellLat, cellLon);
            if (interpolatedPrice !== null) {
                avgSqftPrice = interpolatedPrice;
                color = getColorForPrice(avgSqftPrice);
                vibeScore = Math.round(calculateVibeScore(avgSqftPrice) * 10) / 10;
                hasRealData = true;
            } else {
                color = 'transparent';
                vibeScore = null;
            }
        }
        
        const polygon = [
            [lon, lat],
            [lon + GRID_SIZE, lat],
            [lon + GRID_SIZE, lat + GRID_SIZE],
            [lon, lat + GRID_SIZE],
            [lon, lat]
        ];
        
        features.push({
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: [polygon]
            },
            properties: {
                id: `cell-${features.length}`,
                vibe_score: vibeScore,
                avg_sqft_price: avgSqftPrice,
                property_count: propertyCount,
                color: color,
                has_real_data: hasRealData,
                center_lat: cellLat,
                center_lon: cellLon
            }
        });
    }
}

const geojson = {
    type: 'FeatureCollection',
    features: features
};

fs.writeFileSync('./grid_data.json', JSON.stringify(geojson, null, 2));

console.log(`Generated grid with ${features.length} cells`);
const cellsWithData = features.filter(f => f.properties.has_real_data).length;
console.log(`Cells with real property data: ${cellsWithData}`);
console.log(`Cells with gradient fallback: ${features.length - cellsWithData}`);
