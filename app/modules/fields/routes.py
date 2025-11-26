from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from shapely.geometry import shape
from geoalchemy2.shape import from_shape, to_shape
from app.core.db import get_db
from .models import Field
from .schemas import FieldCreateByShape, FieldOut
from .services.shapes import (
    circle_to_polygon, rectangle_to_polygon,
    semicircle_to_polygon, polygon_passthrough
)

router = APIRouter()

@router.post("/", response_model=FieldOut)
def create_field(payload: FieldCreateByShape, db: Session = Depends(get_db)):
    if payload.shape == "circle":
        d = payload.data
        poly_geojson = circle_to_polygon(d.center_lat, d.center_lon, d.radius_m, d.num_points or 64)
    elif payload.shape == "rectangle":
        d = payload.data
        poly_geojson = rectangle_to_polygon(d.lat1, d.lon1, d.lat2, d.lon2)
    elif payload.shape == "semicircle":
        d = payload.data
        poly_geojson = semicircle_to_polygon(d.center_lat, d.center_lon, d.radius_m, d.direction, d.num_points or 64)
    elif payload.shape == "polygon":
        d = payload.data
        poly_geojson = polygon_passthrough(d.boundary_geojson)
    else:
        raise HTTPException(400, "Unsupported shape")

    try:
        polygon = shape(poly_geojson)
        geom = from_shape(polygon, srid=4326)
    except Exception:
        raise HTTPException(400, "Invalid polygon after conversion")

    field = Field(name=payload.name, boundary=geom, area_ha=payload.area_ha or 0)
    db.add(field); db.commit(); db.refresh(field)

    return FieldOut(
        id=field.id, name=field.name,
        boundary_geojson=poly_geojson,
        area_ha=field.area_ha
    )

@router.get("/{field_id}", response_model=FieldOut)
def get_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    polygon = to_shape(field.boundary)
    return FieldOut(
        id=field.id, name=field.name,
        boundary_geojson=polygon.__geo_interface__,
        area_ha=field.area_ha
    )
