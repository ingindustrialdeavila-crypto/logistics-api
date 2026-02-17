from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Database
from app.database import engine, Base

# Import models (for table creation)
from app.models.user import User
from app.models.order import Order
from app.models.driver import Driver
from app.models.order_status_history import OrderStatusHistory

# Routers
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.orders import router as orders_router
from app.routers.drivers import router as drivers_router


# Create DB tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI app
app = FastAPI(
    title="MLOGIX API",
    version="1.0.0",
    description="API empresarial para logística y mensajería"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambiar en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files (images, css, js)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Templates (HTML)
templates = Jinja2Templates(directory="app/templates")


# Root endpoint
@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "MLOGIX API running"
    }


# Home page (HTML)
@app.get("/home")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# Include routers
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orders_router)
app.include_router(drivers_router)


# Global exception handler (optional but recommended)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )