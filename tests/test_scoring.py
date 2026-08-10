import datetime
from app import models
from app.services.scoring import score_timeline


def make_record(**overrides):
    defaults = dict(
        date_time=datetime.datetime(2026, 8, 6, 12, 0),
        temperature_c=25.0,
        wind_speed_kn=3.0,          # calm
        precipitation_probability=0.0,
        cloud_cover_percentage=0.0,
        wave_height_m=0.05,         # flat
        wave_period_sec=3.0,
        wave_direction=180.0,
        tide_height_ft=1.5,
    )
    defaults.update(overrides)
    return models.MergedData(**defaults)

def test_calm_conditions_score_100():
    scores = score_timeline([make_record()])
    assert scores[0].score == 100
    assert scores[0].txt_rating == "Excellent"


def test_high_wind_caps_at_40():
    # wind 25 -> (25-6)*5 = 95, but capped at 40, so 100 - 40 = 60
    scores = score_timeline([make_record(wind_speed_kn=25)])
    assert scores[0].score == 60
    assert scores[0].txt_rating == "Fair"

def test_missing_wave_data_does_not_crash():
    scores = score_timeline([make_record(wave_height_m=None)])
    assert scores[0].score == 100
    assert scores[0].txt_rating == "Excellent"


def test_high_precip_is_capped_at_20():
    scores = score_timeline([make_record(precipitation_probability=100)])
    # precip penalty caps at 20, so 100 - 20 = 80
    assert scores[0].score == 80
    assert scores[0].txt_rating == "Good"


def test_score_90_boundary_is_excellent():
    # (wind - 6) * 5 = 10  ->  wind = 8  ->  score exactly 90
    scores = score_timeline([make_record(wind_speed_kn=8)])
    assert scores[0].score == 90
    assert scores[0].txt_rating == "Excellent"


def test_penalties_from_multiple_factors_stack():
    # wind 12 -> (12-6)*5 = 30 ;  precip 40 -> (40-10)*0.5 = 15 ;  100-30-15 = 55
    scores = score_timeline([make_record(wind_speed_kn=12, precipitation_probability=40)])
    assert scores[0].score == 55
    assert scores[0].txt_rating == "Fair"