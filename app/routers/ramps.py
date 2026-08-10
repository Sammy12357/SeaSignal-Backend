import json
from pathlib import Path
from fastapi import APIRouter
from app import models
from app.providers import nws_alerts
from app.services import timeline, scoring
from scripts.explore_api import haver_sine

router = APIRouter()

#catalog file path
CATALOG = Path(__file__).resolve().parent.parent.parent / "catalog_pipeline" / "catalog.json"
_raw = json.loads(CATALOG.read_text(encoding="utf-8"))
RAMPS = [models.Ramp(**item) for item in _raw]

# Find the nearest ramps to a given latitude and longitude
def nearest_ramps(lat, lon, limit):
    results = []
    for ramp in RAMPS:
        distance = haver_sine(lat, lon, ramp.latitude, ramp.longitude)
        results.append(ramp.model_copy(update={"distance_km": round(distance, 2)}))
    results.sort(key=lambda r: r.distance_km)
    return results[:limit]

# Get the nearest ramps to a given location
@router.get("/ramps", response_model=list[models.Ramp])
def get_ramps(lat: float, lon: float, limit: int = 5):
    return nearest_ramps(lat, lon, limit)

# Get a boating plan for a given location, including the nearest ramps, best forecast window, and alerts
@router.get("/plan", response_model=list[models.RampPlan])
def get_plan(lat: float, lon: float, limit: int = 3):
    ramps = nearest_ramps(lat, lon, limit)
    results = []
    for ramp in ramps:
        scores = scoring.score_location(ramp.latitude, ramp.longitude)   # ← cached
        daytime = [s for s in scores if 6 <= s.date_time.hour <= 20]
        if not daytime:
            continue
        best = max(daytime, key=lambda s: s.score)
        alerts = nws_alerts.fetch_alerts(ramp.latitude, ramp.longitude)
        results.append(models.RampPlan(ramp=ramp, best_window=best, alerts=alerts))
    return results