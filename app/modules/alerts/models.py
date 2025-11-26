from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.core.db import Base
import datetime as dt

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id"), index=True)
    result_id = Column(Integer, ForeignKey("ndvi_results.id"), nullable=True)
    type = Column(String)
    message = Column(String)
    severity = Column(String, default="medium")
    created_at = Column(DateTime, default=dt.datetime.utcnow)
