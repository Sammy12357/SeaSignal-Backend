from pathlib import Path
import json
import httpx

FIXTURES_DIR = Path(__file__).resolve().parent.parent /"tests" / "fixtures"

HEADERS = {"User-Agent": "SeaSignal/1.0 (contact: restreposamuel2004@gmail.com)"}

FIXTURES_DIR.mkdir(parents=True, exist_ok=True)

print(f"Fixtures directory: {FIXTURES_DIR}")

BALLAST_POINT = (27.89, -82.49)

#savce the given data as a JSON fixture file in the fixtures directory
def save_fixture(filename, data):
    file_path = FIXTURES_DIR / filename
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        print(f"Saved fixture: {file_path}")

#explore the forecast data for a given latitude and longitude, fetching hourly temperature, precipitation probability, cloud cover, and wind speed for the next 7 days
def explore_forecast(lat,lon):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation_probability,cloudcover,windspeed_10m",
        "windspeed_unit": "kn",
        "timezone": "auto",
        "forecast_days": 7
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data= response.json()
    print(data.keys())
    print(data["hourly"].keys())
    print(data["hourly"]["time"][0:3])
    print(data["hourly"]["windspeed_10m"][0:3])
    print(len(data["hourly"]["time"]))
    print(len(data["hourly"]["windspeed_10m"]))
    print(data["hourly_units"])
    print(data["timezone"])
    print(data["utc_offset_seconds"])

    save_fixture("meteo_forecast.json", data)


#explore the marine data for a given latitude and longitude, fetching hourly wave height, wave period, and wave direction for the next 7 days
def explore_marine(lat, lon):
    url = "https://marine-api.open-meteo.com/v1/marine"

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wave_height,wave_period,wave_direction",
        "timezone": "auto",
        "forecast_days": 7,
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    print(data.keys())
    print(data["hourly"].keys())
    print(data["hourly"]["time"][0:3])
    print(data["hourly"]["wave_height"][0:3])
    print(data["hourly"]["wave_period"][0:3])
    print(data["hourly"]["wave_direction"][0:3])
    print(len(data["hourly"]["time"]))
    print(len(data["hourly"]["wave_height"]))
    print(data["hourly_units"])
    print(data["timezone"])
    print(data["utc_offset_seconds"])

    z = 0
    for i in range(len(data["hourly"]["wave_height"])):
        if data["hourly"]["wave_height"][i] is None:
            z += 1
    print(f"Number of None values in wave_height: {z}")

    save_fixture("meteo_marine.json", data)


# Fetch tide stations from the NOAA API
def fetch_stations():
    url = "https://api.tidesandcurrents.noaa.gov/mdapi/prod/webapi/stations.json"

    params = {
        "type": "tidepredictions"
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    print(data.keys())
    print(len(data["stations"]))
    print(data["stations"][0:3])

    save_fixture("noaa_stations.json", data)

#haversine formula to calculate the great-circle distance between two points on the Earth given their latitude and longitude
def haver_sine(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371.0  # Radius of the Earth in kilometers

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

# Find the nearest station to a given latitude and longitude
def find_nearest_station(lat, lon, stations):
    nearest_station = None
    min_distance = float('inf')

    for station in stations:
        station_lat = station.get("lat")
        station_lon = station.get("lng")

        if station_lat is not None and station_lon is not None:
            distance = haver_sine(lat, lon, station_lat, station_lon)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station

    save_fixture("nearest_station.json", nearest_station)
    return nearest_station

# Fetch tide predictions for a given station and date range
def fetch_tide_predictions(station_id, begin_date, end_date):
    url = f"https://api.tidesandcurrents.noaa.gov/api/prod/datagetter"

    params = {
        "station": station_id,
        "begin_date": begin_date,
        "end_date": end_date,
        "product": "predictions",
        "datum": "MLLW",
        "units": "english",
        "time_zone": "lst_ldt",
        "format": "json",
        "interval": "h"  
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    print(data.keys())
    print(len(data["predictions"]))
    print(data["predictions"][0:3])

    save_fixture(f"noaa_tide_predictions_{station_id}_{begin_date}_{end_date}.json", data)

if __name__ == "__main__":
    explore_forecast(*BALLAST_POINT)
    explore_marine(*BALLAST_POINT)
    fetch_stations()
    print(find_nearest_station(*BALLAST_POINT, json.load(open(FIXTURES_DIR / "noaa_stations.json"))["stations"]))  
    fetch_tide_predictions("8726639", "20240101", "20240107")  