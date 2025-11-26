from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime as dt

class SatelliteImage(Base):
    __tablename__ = "satellite_images"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id"), index=True, nullable=False)
    source = Column(String, default="sentinel2")
    captured_at = Column(DateTime, index=True)
    red_path = Column(String, nullable=False)
    nir_path = Column(String, nullable=False)
    cloud_percent = Column(Float, default=0)
    meta = Column(JSON, default={})
    field = relationship("Field", back_populates="satellite_images")
    ndvi_results = relationship("NDVIResult", back_populates="image")

class NDVIResult(Base):
    __tablename__ = "ndvi_results"
    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey("satellite_images.id"), index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), index=True)
    processed_at = Column(DateTime, default=dt.datetime.utcnow)
    mean_ndvi = Column(Float)
    min_ndvi = Column(Float)
    max_ndvi = Column(Float)
    ndvi_tif_path = Column(String)
    ndvi_png_path = Column(String, nullable=True)
    stats = Column(JSON, default={})
    image = relationship("SatelliteImage", back_populates="ndvi_results")
    field = relationship("Field", back_populates="ndvi_results")

class ChangeDetectionResult(Base):
    __tablename__ = "change_detection_results"
    id = Column(Integer, primary_key=True)
    field_id = Column(Integer, ForeignKey("fields.id"), index=True)
    old_ndvi_id = Column(Integer, ForeignKey("ndvi_results.id"))
    new_ndvi_id = Column(Integer, ForeignKey("ndvi_results.id"))
    processed_at = Column(DateTime, default=dt.datetime.utcnow)
    delta_tif_path = Column(String)
    stats = Column(JSON, default={})
    field = relationship("Field")
