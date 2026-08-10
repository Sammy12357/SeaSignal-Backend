import httpx
from app import config, models

HEADERS = config.HEADERS

# Fetch alerts from NWS API
def fetch_alerts(lat, lon):
    url = config.urls["nws_alerts"]
    params = {"point": f"{lat},{lon}"}
    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return parse_alerts(data)

# Parse the alerts data into a list of Alert models
def parse_alerts(data):
    features = data.get("features", [])
    alerts = []
    for feature in features:
        props = feature.get("properties", {})
        alerts.append(models.Alert(
            event=props.get("event"),
            headline=props.get("headline"),
            severity=props.get("severity"),
            onset=props.get("onset"),
            expires=props.get("expires"),
            area_desc=props.get("areaDesc"),
        ))
    return alerts

if __name__ == "__main__":
    lat = 38.8977
    lon = -77.0365
    alerts = fetch_alerts(lat, lon)
    print(f"{len(alerts)} active alerts")
    for alert in alerts:
        print(alert)