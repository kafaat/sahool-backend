# Sahool Mega (Satellite + Weather + Shapes + Flutter/Web UI)

This repo contains:
- FastAPI backend with PostGIS, Celery, CDSE Sentinel-2 ingestion
- NDVI processing (windowed), PNG previews, XYZ tiles, legend
- Change detection (delta NDVI), NDVI-drop alerts
- Field shapes support: circle, rectangle, polygon, semicircle -> stored as Polygon
- Free weather integration using Open-Meteo (no API key)
- Minimal Flutter page and Web page for drawing fields + viewing NDVI tiles

## Quickstart (local)
1. Copy `.env.example` -> `.env` and fill CDSE credentials.
2. `docker compose up --build -d`
3. Init DB: 
   `docker compose exec api alembic revision --autogenerate -m "init"`
   `docker compose exec api alembic upgrade head`
4. Swagger: http://localhost:8000/docs

## Flutter UI
See `ui/flutter/README.md`.

## Web UI
See `ui/web/README.md`.
