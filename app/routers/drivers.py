from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.driver import Driver
from app.schemas import DriverCreate, DriverUpdate, DriverOut
from app.dependencies import require_role


router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"]
)


# =========================
# CREATE DRIVER (ADMIN)
# =========================
@router.post("/", response_model=DriverOut)
def create_driver(
    data: DriverCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):

    # Verificar que el usuario exista
    user_exists = db.query(User)\
        .filter(User.id == data.user_id)\
        .first()

    if not user_exists:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    driver = Driver(**data.dict())

    db.add(driver)
    db.commit()
    db.refresh(driver)

    return driver


# =========================
# GET ALL DRIVERS (ADMIN)
# =========================
@router.get("/", response_model=List[DriverOut])
def get_drivers(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return db.query(Driver).all()


# =========================
# GET DRIVER BY ID
# =========================
@router.get("/{driver_id}", response_model=DriverOut)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db)
):
    driver = db.query(Driver)\
        .filter(Driver.id == driver_id)\
        .first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver no existe")

    return driver


# =========================
# UPDATE DRIVER (ADMIN)
# =========================
@router.put("/{driver_id}", response_model=DriverOut)
def update_driver(
    driver_id: int,
    updated_data: DriverUpdate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):

    driver = db.query(Driver)\
        .filter(Driver.id == driver_id)\
        .first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver no existe")

    for key, value in updated_data.dict(exclude_unset=True).items():
        setattr(driver, key, value)

    db.commit()
    db.refresh(driver)

    return driver


# =========================
# DELETE DRIVER (ADMIN)
# =========================
@router.delete("/{driver_id}")
def delete_driver(
    driver_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):

    driver = db.query(Driver)\
        .filter(Driver.id == driver_id)\
        .first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver no existe")

    db.delete(driver)
    db.commit()

    return {"message": "Driver eliminado correctamente"}


# =========================
# CHANGE AVAILABILITY (ADMIN)
# =========================
@router.patch("/{driver_id}/availability", response_model=DriverOut)
def change_status(
    driver_id: int,
    status: bool,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):

    driver = db.query(Driver)\
        .filter(Driver.id == driver_id)\
        .first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver no existe")

    driver.is_active = status

    db.commit()
    db.refresh(driver)

    return driver