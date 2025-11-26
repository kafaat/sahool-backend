from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.modules.alerts.models import Alert

router = APIRouter()

@router.get("/")
def list_alerts(field_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Alert)
        .filter(Alert.field_id == field_id)
        .order_by(Alert.created_at.desc()).all()
    )
