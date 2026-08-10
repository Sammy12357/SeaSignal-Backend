import httpx
from app import config
from app import models

HEADERS = config.HEADERS

def fetch_forecast(lat,lon):

    url = config.urls["forecast"]
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

    return parse_forecast(data)

def parse_forecast(data):
    hourly_data = data.get("hourly", {})
    time_list = hourly_data.get("time", [])
    temperature_list = hourly_data.get("temperature_2m", [])
    windspeed_list = hourly_data.get("windspeed_10m", [])
    precipitation_list = hourly_data.get("precipitation_probability", [])
    cloudcover_list = hourly_data.get("cloudcover", [])

    forecast_hourly_list = []
    for time, temperature, windspeed, precipitation, cloudcover in zip(time_list, temperature_list, windspeed_list, precipitation_list, cloudcover_list):
        forecast_hourly = models.ForecastHourly(
            date_time=time,
            temperature_c=temperature,
            wind_speed_kn=windspeed,
            precipitation_probability=precipitation,
            cloud_cover_percentage=cloudcover
        )
        forecast_hourly_list.append(forecast_hourly)

    return forecast_hourly_list

def fetch_marine(lat, lon):
    url = config.urls["marine"]
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "wave_height,wave_direction,wave_period",
        "timezone": "auto",
        "forecast_days": 7
    }

    response = httpx.get(url, params=params, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    return parse_marine(data)

def parse_marine(data):
    hourly_data = data.get("hourly", {})
    time_list = hourly_data.get("time", [])
    wave_height_list = hourly_data.get("wave_height", [])
    wave_direction_list = hourly_data.get("wave_direction", [])
    wave_period_list = hourly_data.get("wave_period", [])

    marine_hourly_list = []
    for time, wave_height, wave_direction, wave_period in zip(time_list, wave_height_list, wave_direction_list, wave_period_list):
        marine_hourly = models.MarineHour(
            date_time=time,
            wave_height_m=wave_height,
            wave_direction=wave_direction,
            wave_period_sec=wave_period
        )
        marine_hourly_list.append(marine_hourly)

    return marine_hourly_list


if __name__ == "__main__":
    lat = 40.7128
    lon = -74.0060
    # forecast = fetch_forecast(lat, lon)
    # for hourly in forecast:
    #     print(hourly)
    marine = fetch_marine(lat, lon)
    for hourly in marine:
        print(hourly)
