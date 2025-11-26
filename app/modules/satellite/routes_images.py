from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import SatelliteImage
from app.workers.tasks import fetch_sentinel_image_task

router = APIRouter()

@router.post("/fetch")
def fetch_latest_image(field_id: int):
    task = fetch_sentinel_image_task.delay(field_id)
    return {"status": "downloading", "task_id": task.id}

@router.get("/")
def list_images(field_id: int, db: Session = Depends(get_db)):
    return (
        db.query(SatelliteImage)
        .filter(SatelliteImage.field_id == field_id)
        .order_by(SatelliteImage.captured_at.desc())
        .all()
    )
