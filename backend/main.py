from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db
from backend.routes.auth import router as auth_router
from backend.routes.devices import router as devices_router
from backend.routes.locations import router as locations_router
from backend.routes.reports import router as reports_router

app = FastAPI(
    title="PhoneGuard API",
    description="Authorized lost and stolen phone management system",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {
        "application": "PhoneGuard",
        "status": "running",
        "message": "PhoneGuard API is working"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


app.include_router(auth_router)
app.include_router(devices_router)
app.include_router(locations_router)
app.include_router(reports_router)