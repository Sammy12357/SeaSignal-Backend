from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import forecast, ramps

app = FastAPI(title="SeaSignal")

#middleware to allow cross-origin requests from any origin, with no credentials, and allowing all methods and headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#include routers for forecast and ramps endpoints
app.include_router(forecast.router)
app.include_router(ramps.router)

#root endpoint that returns basic information about the service, including the name, documentation URL, and available endpoints
@app.get("/")
def root():
    return {"service": "SeaSignal", "docs": "/docs", "endpoints": ["/forecast", "/ramps", "/plan"]}
