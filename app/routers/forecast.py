from fastapi import APIRouter
from app import models
from app.services import timeline, scoring

router = APIRouter()

@router.get("/forecast", response_model=list[models.ConditionScore])
def get_forecast(lat: float, lon: float):
    return scoring.score_location(lat, lon)

from app.providers import nws_alerts   # add to the imports at top

@router.get("/alerts", response_model=list[models.Alert])
def get_alerts(lat: float, lon: float):
    return nws_alerts.fetch_alerts(lat, lon)