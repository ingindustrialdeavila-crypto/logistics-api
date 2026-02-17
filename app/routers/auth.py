from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")

    if not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    return RedirectResponse(url="/admin", status_code=302)