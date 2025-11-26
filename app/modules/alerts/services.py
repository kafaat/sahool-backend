from sqlalchemy.orm import Session
from app.modules.satellite.models import NDVIResult
from app.modules.alerts.models import Alert

def generate_ndvi_drop_alert(db: Session, field_id: int, new_result_id: int, threshold_drop=0.1):
    results = (
        db.query(NDVIResult)
        .filter(NDVIResult.field_id == field_id)
        .order_by(NDVIResult.processed_at.desc())
        .limit(2).all()
    )
    if len(results) < 2: return None
    new_r, old_r = results[0], results[1]
    drop = (old_r.mean_ndvi or 0) - (new_r.mean_ndvi or 0)
    if drop >= threshold_drop:
        severity = "high" if drop >= 0.2 else "medium"
        alert = Alert(
            field_id=field_id,
            result_id=new_result_id,
            type="ndvi_drop",
            message=f"NDVI dropped by {drop:.2f} compared to previous image.",
            severity=severity
        )
        db.add(alert); db.commit()
        return alert.id
    return None
