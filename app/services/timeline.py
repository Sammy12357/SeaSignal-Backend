from app.providers import open_meteo, noaa_tides
from app import models
from app import config
from datetime import date, timedelta

open_meteo_service = open_meteo
noaa_tides_service = noaa_tides

#Here we build the timeline data by merging forecast, marine, and tide data, for a full 24 hour block
def build_timeline(lat,lon):
    forecast_data = open_meteo_service.fetch_forecast(lat, lon)
    marine_data = open_meteo_service.fetch_marine(lat, lon)

    stations_data = noaa_tides_service.fetch_stations()
    nearest_station = noaa_tides_service.find_nearest_station(lat, lon, stations_data)

    begin_date = date.today().strftime("%Y%m%d")
    end_date = (date.today() + timedelta(days=6)).strftime("%Y%m%d")
    tide_predictions = noaa_tides_service.fetch_tide_predictions(nearest_station.id, begin_date, end_date)

    marine_by_time = {mp.date_time: mp for mp in marine_data}
    tide_by_time = {tp.date_time: tp for tp in tide_predictions}

    merged_list = []
    for forecast in forecast_data:
        marine = marine_by_time.get(forecast.date_time)
        tide = tide_by_time.get(forecast.date_time)

        if marine:
            merged_data = models.MergedData(
                date_time=forecast.date_time,
                temperature_c=forecast.temperature_c,
                wind_speed_kn=forecast.wind_speed_kn,
                precipitation_probability=forecast.precipitation_probability,
                cloud_cover_percentage=forecast.cloud_cover_percentage,
                wave_height_m=marine.wave_height_m,
                wave_direction=marine.wave_direction,
                wave_period_sec=marine.wave_period_sec,
                tide_height_ft=tide.height_ft if tide else None
            )
            merged_list.append(merged_data)

    return merged_list

# Print a timeline table of merged data records, showing time, temperature, wind speed, wave height, tide height, and precipitation probability
def print_timeline_table(records, limit=24):
    header = f"{'Time':<12}{'Temp°C':>8}{'Wind kn':>9}{'Wave m':>8}{'Tide ft':>9}{'Precip%':>9}"
    print(header)
    print("-" * len(header))
    for r in records[:limit]:
        time_str = r.date_time.strftime("%m-%d %H:%M")
        wave_str = f"{r.wave_height_m:>8.2f}" if r.wave_height_m is not None else f"{'--':>8}"
        print(
            f"{time_str:<12}"
            f"{r.temperature_c:>8.1f}"
            f"{r.wind_speed_kn:>9.1f}"
            f"{wave_str}"
            f"{r.tide_height_ft:>9.2f}"
            f"{r.precipitation_probability:>9.0f}"
        )

if __name__ == "__main__":
    merged_list = build_timeline(*config.BALLAST_POINT)
    print_timeline_table(merged_list)
