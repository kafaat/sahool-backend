from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.modules.fields.routes import router as fields_router
from app.modules.satellite.routes_images import router as images_router
from app.modules.satellite.routes_ndvi import router as ndvi_router
from app.modules.satellite.routes_ndvi_tiles import router as tiles_router
from app.modules.satellite.routes_legend import router as legend_router
from app.modules.satellite.routes_change import router as change_router
from app.modules.satellite.routes_timeline import router as timeline_router
from app.modules.reports.routes import router as reports_router
from app.modules.alerts.routes import router as alerts_router
from app.modules.weather.routes import router as weather_router

app = FastAPI(title="Sahool Mega")

os.makedirs("storage", exist_ok=True)
app.mount("/storage", StaticFiles(directory="storage"), name="storage")

app.include_router(fields_router, prefix="/fields", tags=["Fields"])
app.include_router(images_router, prefix="/satellite/images", tags=["Satellite Images"])
app.include_router(ndvi_router, prefix="/satellite/ndvi", tags=["NDVI"])
app.include_router(tiles_router, prefix="/satellite/ndvi", tags=["NDVI Tiles"])
app.include_router(legend_router, prefix="/satellite/ndvi", tags=["NDVI Legend"])
app.include_router(change_router, prefix="/satellite/change", tags=["Change Detection"])
app.include_router(timeline_router, prefix="/satellite/ndvi", tags=["NDVI Timeline"])
app.include_router(alerts_router, prefix="/alerts", tags=["Alerts"])
app.include_router(weather_router, prefix="/weather", tags=["Weather (Open-Meteo)"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"])