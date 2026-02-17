from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database
from app.database import engine, Base

# Import models
from app.models.user import User
from app.models.order import Order
from app.models.driver import Driver
from app.models.order_status_history import OrderStatusHistory

# Routers
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.orders import router as orders_router
from app.routers.drivers import router as drivers_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="MLOGIX API",
    version="1.0.0",
    description="API empresarial para logística y mensajería"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


# HOME HTML
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# HEALTH CHECK
@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "message": "MLOGIX API running"
    }


# Routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(drivers_router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )