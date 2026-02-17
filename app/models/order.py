from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship

driver = relationship("Driver", back_populates="orders")

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    pickup_address = Column(String(255), nullable=False)
    delivery_address = Column(String(255), nullable=False)
    status = Column(String(50), default="pending")
    price = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

status_history = relationship(
    "OrderStatusHistory",
    back_populates="order",
    cascade="all, delete-orphan"
)