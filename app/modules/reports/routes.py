from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.satellite.models import NDVIResult, SatelliteImage
from app.modules.alerts.models import Alert

router = APIRouter()

@router.get("/weekly")
def weekly_report(field_id: int, db: Session = Depends(get_db)):
    ndvi = (
        db.query(NDVIResult)
        .filter(NDVIResult.field_id == field_id)
        .order_by(NDVIResult.processed_at.desc())
        .limit(4)
        .all()
    )
    alerts = (
        db.query(Alert)
        .filter(Alert.field_id == field_id)
        .order_by(Alert.created_at.desc())
        .limit(10)
        .all()
    )
    return {
        "field_id": field_id,
        "ndvi_last_weeks": [
            {"date": r.processed_at.isoformat(), "mean": r.mean_ndvi, "min": r.min_ndvi, "max": r.max_ndvi, "png": r.ndvi_png_path}
            for r in ndvi
        ],
        "alerts": [
            {"date": a.created_at.isoformat(), "type": a.type, "severity": a.severity, "message": a.message}
            for a in alerts
        ],
        "note": "Client can render this into PDF."
    }
