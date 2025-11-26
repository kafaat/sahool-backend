from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime as dt

class Farm(Base):
    __tablename__ = "farms"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_name = Column(String, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)
    
    fields = relationship("Field", back_populates="farm")
