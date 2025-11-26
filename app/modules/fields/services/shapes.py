import math
from shapely.geometry import Point, Polygon
from shapely.ops import transform
from pyproj import CRS, Transformer

def _local_aeqd_transformer(lat: float, lon: float):
    aeqd = CRS.from_proj4(
        f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m +no_defs"
    )
    wgs84 = CRS.from_epsg(4326)
    to_aeqd = Transformer.from_crs(wgs84, aeqd, always_xy=True).transform
    to_wgs84 = Transformer.from_crs(aeqd, wgs84, always_xy=True).transform
    return to_aeqd, to_wgs84

def circle_to_polygon(lat: float, lon: float, radius_m: float, num_points: int = 64):
    to_aeqd, to_wgs84 = _local_aeqd_transformer(lat, lon)
    center_wgs = Point(lon, lat)
    center_m = transform(to_aeqd, center_wgs)
    circle_m = center_m.buffer(radius_m, resolution=max(8, num_points // 4))
    circle_wgs = transform(to_wgs84, circle_m)
    return circle_wgs.__geo_interface__

def rectangle_to_polygon(lat1: float, lon1: float, lat2: float, lon2: float):
    min_lat, max_lat = sorted([lat1, lat2])
    min_lon, max_lon = sorted([lon1, lon2])
    poly = Polygon([
        (min_lon, min_lat),
        (min_lon, max_lat),
        (max_lon, max_lat),
        (max_lon, min_lat),
        (min_lon, min_lat),
    ])
    return poly.__geo_interface__

def semicircle_to_polygon(lat: float, lon: float, radius_m: float,
                          direction: str = "up", num_points: int = 64):
    to_aeqd, to_wgs84 = _local_aeqd_transformer(lat, lon)
    center_wgs = Point(lon, lat)
    center_m = transform(to_aeqd, center_wgs)

    start_angle = {
        "up": math.pi,
        "down": 0.0,
        "left": -math.pi/2,
        "right": math.pi/2,
    }.get(direction, math.pi)

    coords_m = []
    for i in range(num_points + 1):
        ang = start_angle - math.pi * (i / num_points)
        x = center_m.x + radius_m * math.cos(ang)
        y = center_m.y + radius_m * math.sin(ang)
        coords_m.append((x, y))

    coords_m.append((center_m.x, center_m.y))
    poly_m = Polygon(coords_m)
    poly_wgs = transform(to_wgs84, poly_m)
    return poly_wgs.__geo_interface__

def polygon_passthrough(geojson_polygon: dict):
    return geojson_polygon
