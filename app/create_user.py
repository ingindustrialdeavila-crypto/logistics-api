from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = SessionLocal()

hashed_password = pwd_context.hash("123456")

new_user = User(
    name="Admin",
    email="admin@mlogix.com",
    password=hashed_password
)

db.add(new_user)
db.commit()
db.close()

print("Usuario creado correctamente")