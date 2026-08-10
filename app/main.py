from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import forecast, ramps

app = FastAPI(title="SeaSignal")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(forecast.router)
app.include_router(ramps.router)


@app.get("/")
def root():
    return {"service": "SeaSignal", "docs": "/docs", "endpoints": ["/forecast", "/ramps", "/plan"]}
