from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

# ==============================
# ENUMS
# ==============================

class UserRole(str, Enum):
    admin = "admin"
    driver = "driver"
    customer = "customer"


class OrderStatus(str, Enum):
    pending = "pending"
    assigned = "assigned"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"


# ==============================
# USER SCHEMAS
# ==============================

class UserBase(BaseModel):
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ==============================
# DRIVER SCHEMAS
# ==============================

class DriverBase(BaseModel):
    name: str
    phone: str
    is_active: bool = True


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


class DriverOut(DriverBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


# ==============================
# ORDER SCHEMAS
# ==============================

class OrderBase(BaseModel):
    pickup_address: str
    delivery_address: str
    status: OrderStatus = OrderStatus.pending


class OrderCreate(OrderBase):
    driver_id: Optional[int] = None


class OrderUpdate(BaseModel):
    pickup_address: Optional[str] = None
    delivery_address: Optional[str] = None
    status: Optional[OrderStatus] = None
    driver_id: Optional[int] = None


class OrderResponse(OrderBase):
    id: int
    driver_id: Optional[int]
    created_at: datetime

    class Config:
        orm_mode = True


# ==============================
# TOKEN SCHEMAS (AUTH)
# ==============================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None

# Alias para evitar error
User = UserResponse

class TokenData(BaseModel):
    email: Optional[str] = None


# 🔥 FIX para evitar AttributeError
User = UserResponse