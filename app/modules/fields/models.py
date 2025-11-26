from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from app.core.db import Base

class Field(Base):
    __tablename__ = "fields"
    id = Column(Integer, primary_key=True)
    farm_id = Column(Integer, ForeignKey("farms.id"), nullable=True)

    name = Column(String, nullable=False)
    boundary = Column(Geometry("POLYGON", srid=4326), nullable=False)
    area_ha = Column(Float, default=0)

    farm = relationship("Farm", back_populates="fields")
    satellite_images = relationship("SatelliteImage", back_populates="field")
    ndvi_results = relationship("NDVIResult", back_populates="field")
