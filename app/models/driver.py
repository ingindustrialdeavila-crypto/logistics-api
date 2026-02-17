from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    status = Column(String, default="available")

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con órdenes
    orders = relationship("Order", back_populates="driver")