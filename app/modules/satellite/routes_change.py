from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import ChangeDetectionResult, NDVIResult
from app.workers.tasks import change_detection_task

router = APIRouter()

@router.post("/process")
def process_change(field_id: int, old_ndvi_id: int, new_ndvi_id: int, db: Session = Depends(get_db)):
    if not db.query(NDVIResult).get(old_ndvi_id) or not db.query(NDVIResult).get(new_ndvi_id):
        raise HTTPException(404, "NDVI results missing")
    task = change_detection_task.delay(field_id, old_ndvi_id, new_ndvi_id)
    return {"status": "processing", "task_id": task.id}

@router.get("/")
def list_changes(field_id: int, db: Session = Depends(get_db)):
    return (
        db.query(ChangeDetectionResult)
        .filter(ChangeDetectionResult.field_id == field_id)
        .order_by(ChangeDetectionResult.processed_at.desc())
        .all()
    )
