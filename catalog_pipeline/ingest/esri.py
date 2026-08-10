import httpx
from app import config, models

# Fetch boat ramps from the FWC Esri API, handling pagination and parsing the response into Ramp models
def fetch_ramps(url, page_size=1000):
    ramps = []
    offset = 0
    while True:
        params = {
            "where": "1=1",                                   
            "outFields": "RampName,County,WaterBodyName,Status",
            "returnGeometry": "true",
            "outSR": "4326",                                  
            "resultOffset": offset,
            "resultRecordCount": page_size,
            "f": "geojson",
        }
        response = httpx.get(url, params=params, headers=config.HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()

        features = data.get("features", [])
        if not features:
            break
        ramps.extend(parse_features(features))

        if not data.get("exceededTransferLimit"):             
            break
        offset += len(features)                              

    return ramps

# Parse the features from the Esri API response into a list of Ramp models
def parse_features(features):
    ramps = []
    for feature in features:
        geom = feature.get("geometry") or {}
        coords = geom.get("coordinates")
        props = feature.get("properties", {})
        if not coords:                                        
            continue
        lon, lat = coords[0], coords[1]                       
        ramps.append(models.Ramp(
            name=props.get("RampName") or "Unknown Ramp",
            latitude=lat,
            longitude=lon,
            county=props.get("County"),
        ))
    return ramps


if __name__ == "__main__":
    url = "https://gis.myfwc.com/mapping/rest/services/Open_Data/FWC_Florida_Boat_Ramp_Inventory/MapServer/4/query"
    ramps = fetch_ramps(url)
    print(f"Fetched {len(ramps)} ramps")
    for r in ramps[:5]:
        print(r)