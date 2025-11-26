import os, zipfile, datetime as dt
from celery import shared_task
from sqlalchemy.orm import Session
from geoalchemy2.shape import to_shape

from app.core.db import SessionLocal
from app.core.config import settings
from app.modules.fields.models import Field
from app.modules.satellite.models import SatelliteImage, NDVIResult, ChangeDetectionResult
from app.modules.satellite.services.cdse_client import (
    get_access_token, search_latest_s2_l2a, download_product
)
from app.modules.satellite.services.ndvi_large import compute_ndvi_windowed
from app.modules.satellite.services.raster_ops import save_ndvi_tif
from app.modules.satellite.services.png_preview import save_ndvi_png
from app.modules.satellite.services.change_detection import compute_delta_ndvi
from app.modules.alerts.services import generate_ndvi_drop_alert

@shared_task
def fetch_sentinel_image_task(field_id: int):
    db: Session = SessionLocal()
    try:
        field = db.query(Field).get(field_id)
        if not field:
            return {"error":"Field not found"}
        polygon = to_shape(field.boundary)
        product = search_latest_s2_l2a(polygon.wkt)
        if not product:
            return {"error":"No sentinel product found"}

        product_id = product["Id"]
        captured_at = product["ContentDate"]["Start"]
        cloud = product.get("cloudCover", 0)

        token = get_access_token()
        out_folder = os.path.join(settings.storage_root, "sentinel", product_id)
        os.makedirs(out_folder, exist_ok=True)
        zip_path = os.path.join(out_folder, f"{product_id}.zip")
        download_product(product_id, zip_path, token)

        red_path = nir_path = None
        with zipfile.ZipFile(zip_path, "r") as z:
            for name in z.namelist():
                if name.endswith(".jp2") and "B04" in name and red_path is None:
                    z.extract(name, out_folder); red_path = os.path.join(out_folder, name)
                if name.endswith(".jp2") and "B08" in name and nir_path is None:
                    z.extract(name, out_folder); nir_path = os.path.join(out_folder, name)

        if not red_path or not nir_path:
            return {"error":"Bands B04/B08 not found"}

        image = SatelliteImage(
            field_id=field.id, source="sentinel2",
            captured_at=captured_at, red_path=red_path, nir_path=nir_path,
            cloud_percent=float(cloud) if cloud else 0.0, meta=product
        )
        db.add(image); db.commit(); db.refresh(image)
        return {"image_id": image.id}
    finally:
        db.close()

@shared_task
def compute_ndvi_task(image_id: int):
    db: Session = SessionLocal()
    try:
        image = db.query(SatelliteImage).get(image_id)
        if not image:
            return {"error":"Image not found"}

        field = db.query(Field).get(image.field_id)
        polygon = to_shape(field.boundary)

        ndvi_arr, transform, profile, stats = compute_ndvi_windowed(
            image.red_path, image.nir_path, polygon
        )

        out_tif = os.path.join(settings.storage_root, "ndvi", f"{image_id}_{dt.date.today()}.tif")
        os.makedirs(os.path.dirname(out_tif), exist_ok=True)
        save_ndvi_tif(ndvi_arr, transform, profile, out_tif)

        out_png = os.path.join(settings.storage_root, "ndvi_previews", f"{image_id}_{dt.date.today()}.png")
        save_ndvi_png(ndvi_arr, out_png)

        result = NDVIResult(
            image_id=image.id, field_id=field.id,
            mean_ndvi=stats["mean"], min_ndvi=stats["min"], max_ndvi=stats["max"],
            ndvi_tif_path=out_tif, ndvi_png_path=out_png, stats=stats
        )
        db.add(result); db.commit(); db.refresh(result)
        generate_ndvi_drop_alert(db, field.id, result.id)
        return {"ndvi_result_id": result.id, "stats": stats}
    finally:
        db.close()

@shared_task
def change_detection_task(field_id: int, old_ndvi_id: int, new_ndvi_id: int):
    db: Session = SessionLocal()
    try:
        old_r = db.query(NDVIResult).get(old_ndvi_id)
        new_r = db.query(NDVIResult).get(new_ndvi_id)
        if not old_r or not new_r:
            return {"error":"NDVI results not found"}

        out_delta = os.path.join(settings.storage_root, "delta_ndvi", f"{old_ndvi_id}_{new_ndvi_id}.tif")
        path, stats = compute_delta_ndvi(old_r.ndvi_tif_path, new_r.ndvi_tif_path, out_delta)

        cd = ChangeDetectionResult(
            field_id=field_id, old_ndvi_id=old_ndvi_id, new_ndvi_id=new_ndvi_id,
            delta_tif_path=path, stats=stats
        )
        db.add(cd); db.commit(); db.refresh(cd)
        return {"change_result_id": cd.id, "stats": stats}
    finally:
        db.close()
