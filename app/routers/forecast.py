from fastapi import APIRouter
from app import models
from app.services import scoring
from app.providers import nws_alerts

router = APIRouter()

#get forecast for a given location
@router.get("/forecast", response_model=list[models.ConditionScore])
def get_forecast(lat: float, lon: float):
    return scoring.score_location(lat, lon)

#get alerts for a given location
@router.get("/alerts", response_model=list[models.Alert])
def get_alerts(lat: float, lon: float):
    return nws_alerts.fetch_alerts(lat, lon)