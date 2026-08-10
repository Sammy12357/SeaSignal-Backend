import httpx
from app import config, models
from scripts.explore_api import haver_sine  

HEADERS = config.HEADERS

def fetch_stations():
    url = config.urls["stations"]

    params = {
        "type": "tidepredictions"
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()
    return data


def find_nearest_station(lat, lon, stations):
    nearest_station = None
    min_distance = float('inf')
    station_list = stations.get("stations", [])
    for station in station_list:
        station_lat = station.get("lat")
        station_lon = station.get("lng")

        if station_lat is not None and station_lon is not None:
            distance = haver_sine(lat, lon, station_lat, station_lon)
            if distance < min_distance:
                min_distance = distance
                nearest_station = station
    return models.Station(name=nearest_station["name"], latitude=nearest_station["lat"], longitude=nearest_station["lng"], distance_km=min_distance, id=nearest_station["id"])


def fetch_tide_predictions(station_id, begin_date, end_date):
    url = config.urls["tide_predictions"]

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
    predictions = data.get("predictions", [])
    tide_predictions = []
    for prediction in predictions:
        date_time = prediction.get("t")
        height_ft = float(prediction.get("v"))
        tide_prediction = models.TidePrediction(date_time=date_time, height_ft=height_ft)
        tide_predictions.append(tide_prediction)
    return tide_predictions

if __name__ == "__main__":
    data = fetch_stations()
    print(data.keys())
    print(len(data["stations"]))
    print(find_nearest_station(34.0, -120.0, data))
    print(fetch_tide_predictions("9410230", "20240101", "20240107"))