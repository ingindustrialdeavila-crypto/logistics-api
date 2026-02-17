from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.order import Order
from app.models.driver import Driver
from app.schemas import OrderResponse, OrderCreate, OrderUpdate, OrderStatus
from app.services.order_service import validate_status_transition


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# ==============================
# GET ALL
# ==============================
@router.get("/", response_model=List[OrderResponse])
def get_orders(
    status: Optional[OrderStatus] = None,
    db: Session = Depends(get_db)
) -> List[OrderResponse]:

    query = db.query(Order)

    if status is not None:
        query = query.filter(Order.status == status.value)

    return query.all()


# ==============================
# GET BY ID
# ==============================
@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


# ==============================
# CREATE
# ==============================
@router.post("/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
) -> OrderResponse:

    new_order = Order(**order.model_dump())

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


# ==============================
# UPDATE (con validación)
# ==============================
@router.put("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    updated_data: OrderUpdate,
    db: Session = Depends(get_db)
) -> OrderResponse:

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    update_data = updated_data.model_dump(exclude_unset=True)

    # VALIDACIÓN DE ESTADO
    if "status" in update_data and update_data["status"] is not None:

        new_status = update_data["status"].value

        validate_status_transition(order.status, new_status)

        order.status = new_status

        del update_data["status"]

    # ACTUALIZAR OTROS CAMPOS
    for key, value in update_data.items():

        if hasattr(value, "value"):
            value = value.value

        setattr(order, key, value)

    db.commit()
    db.refresh(order)

    return order


# ==============================
# ASSIGN DRIVER (EMPRESARIAL)
# ==============================
@router.post("/{order_id}/assign/{driver_id}")
def assign_driver(
    order_id: int,
    driver_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(Order.id == order_id).first()
    driver = db.query(Driver).filter(Driver.id == driver_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    if driver is None:
        raise HTTPException(status_code=404, detail="Driver not found")

    # Solo órdenes pendientes
    if order.status != "pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be assigned"
        )

    # Solo conductores disponibles
    if driver.status != "available":
        raise HTTPException(
            status_code=400,
            detail="Driver is not available"
        )

    order.driver_id = driver.id
    order.status = "assigned"
    driver.status = "busy"

    db.commit()

    return {
        "message": "Driver assigned successfully",
        "order_id": order.id,
        "driver_id": driver.id
    }


# ==============================
# DELETE
# ==============================
@router.delete("/{order_id}")
def delete_order(order_id: int, db: Session = Depends(get_db)) -> dict:

    order = db.query(Order).filter(Order.id == order_id).first()

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()

    return {"message": "Order deleted successfully"}