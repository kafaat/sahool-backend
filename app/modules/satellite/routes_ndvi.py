from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import NDVIResult, SatelliteImage
from app.workers.tasks import compute_ndvi_task

router = APIRouter()

@router.post("/process")
def process_ndvi(image_id: int, db: Session = Depends(get_db)):
    image = db.query(SatelliteImage).get(image_id)
    if not image:
        raise HTTPException(404, "SatelliteImage not found")
    task = compute_ndvi_task.delay(image_id)
    return {"status": "processing", "task_id": task.id}

@router.get("/")
def list_ndvi(field_id: int, db: Session = Depends(get_db)):
    return (
        db.query(NDVIResult)
        .filter(NDVIResult.field_id == field_id)
        .order_by(NDVIResult.processed_at.desc())
        .all()
    )

@router.get("/{result_id}")
def get_ndvi(result_id: int, db: Session = Depends(get_db)):
    r = db.query(NDVIResult).get(result_id)
    if not r:
        raise HTTPException(404, "NDVIResult not found")
    return r
