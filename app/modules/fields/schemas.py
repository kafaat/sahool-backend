from pydantic import BaseModel
from typing import Any, Literal, Union, Optional

class CircleData(BaseModel):
    center_lat: float
    center_lon: float
    radius_m: float
    num_points: Optional[int] = 64

class RectData(BaseModel):
    lat1: float
    lon1: float
    lat2: float
    lon2: float

class SemiCircleData(BaseModel):
    center_lat: float
    center_lon: float
    radius_m: float
    direction: Literal["up", "down", "left", "right"] = "up"
    num_points: Optional[int] = 64

class PolygonData(BaseModel):
    boundary_geojson: Any

class FieldCreateByShape(BaseModel):
    name: str
    area_ha: Optional[float] = 0
    shape: Literal["circle", "rectangle", "semicircle", "polygon"]
    data: Union[CircleData, RectData, SemiCircleData, PolygonData]

class FieldOut(BaseModel):
    id: int
    name: str
    boundary_geojson: Any
    area_ha: float
    class Config:
        from_attributes = True
