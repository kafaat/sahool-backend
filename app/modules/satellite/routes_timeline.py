from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import NDVIResult

router = APIRouter()

@router.get("/timeline")
def ndvi_timeline(field_id: int, limit: int = 20, db: Session = Depends(get_db)):
    results = (
        db.query(NDVIResult)
        .filter(NDVIResult.field_id == field_id)
        .order_by(NDVIResult.processed_at.asc())
        .limit(limit)
        .all()
    )
    return [
        {"date": r.processed_at.isoformat(), "mean": r.mean_ndvi, "min": r.min_ndvi, "max": r.max_ndvi, "id": r.id}
        for r in results
    ]
