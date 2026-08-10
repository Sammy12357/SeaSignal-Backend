import datetime
from pydantic import BaseModel


class TidePrediction(BaseModel):
    date_time: datetime.datetime
    height_ft: float

class ForecastHourly(BaseModel):
    date_time: datetime.datetime
    temperature_c: float
    wind_speed_kn: float
    precipitation_probability: float
    cloud_cover_percentage: float

class MarineHour(BaseModel):
    date_time: datetime.datetime
    wave_height_m: float | None =None
    wave_period_sec: float | None = None
    wave_direction: float | None = None

class Station(BaseModel):
    name: str
    latitude: float
    longitude: float
    distance_km: float | None = None
    id: str

class ConditionScore(BaseModel):
    date_time : datetime.datetime
    score: int
    txt_rating: str

class MergedData(BaseModel):
    date_time: datetime.datetime
    temperature_c: float
    wind_speed_kn: float
    precipitation_probability: float
    cloud_cover_percentage: float
    wave_height_m: float | None = None
    wave_period_sec: float | None = None
    wave_direction: float | None = None
    tide_height_ft: float | None = None

class Ramp(BaseModel):
    name: str
    latitude: float
    longitude: float
    county: str | None = None
    distance_km: float | None = None

class Alert(BaseModel):
    event: str
    headline: str | None = None
    severity: str | None = None
    onset: datetime.datetime | None = None
    expires: datetime.datetime | None = None
    area_desc: str | None = None

class RampPlan(BaseModel):
    ramp: Ramp
    best_window: ConditionScore
    alerts: list[Alert] = []

if __name__ == "__main__":
    print(TidePrediction(date_time="2024-01-01 00:00", height_ft="1.135"))
    print(ForecastHourly(date_time="2024-01-01 00:00", temperature_c="20.5", wind_speed_kn="15.0", precipitation_probability="0.2", cloud_cover_percentage="75.0"))
    print(MarineHour(date_time="2024-01-01 00:00", wave_height_m=None, wave_period_sec=None, wave_direction=None))
    print(Station(name="Test Station", latitude=34.0, longitude=-120.0, distance_km=None, id="test_station"))
    print(ConditionScore(date_time="2024-01-01 00:00", score=85, txt_rating="Good"))
    print(Ramp(name="Test Ramp", latitude=34.0, longitude=-120.0, distance_km=None, county=None))