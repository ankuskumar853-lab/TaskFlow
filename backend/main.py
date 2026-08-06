import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# Import models so SQLAlchemy creates tables
import models

# Import routers
from routes import users
from routes import projects
from routes import tasks
from routes import algorithms
from routes import quick_add

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskFlow API",
    version="1.0.0",
    description="AI Assisted Task Management Platform"
)

@app.middleware("http")
async def log_requests(request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        print("ERROR:", e)
        raise

# =========================
# CORS Configuration
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# =========================
# Logging Middleware
# =========================
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} - {process_time:.2f} ms"
    )

    return response

# =========================
# Home Route
# =========================
@app.get("/")
def home():
    return {
        "message": "Welcome to TaskFlow API"
    }

# =========================
# Include Routers
# =========================
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(tasks.router)
app.include_router(algorithms.router)
app.include_router(quick_add.router)