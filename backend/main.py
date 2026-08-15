import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base

# ==========================================
# IMPORT MODELS
# ==========================================

import models


# ==========================================
# IMPORT ROUTERS
# ==========================================

from routes import users
from routes import projects
from routes import tasks
from routes import algorithms
from routes import quick_add


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(

    title="TaskFlow API",

    version="1.0.0",

    description=(
        "AI Assisted Task Management Platform"
    )
)


# ==========================================
# CORS CONFIGURATION
# ==========================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=False,

    allow_methods=["*"],

    allow_headers=["*"]
)


# ==========================================
# LOGGING MIDDLEWARE
# ==========================================

@app.middleware("http")
async def log_requests(
    request,
    call_next
):

    start_time = time.time()

    try:

        response = await call_next(
            request
        )

        process_time = (
            time.time() - start_time
        ) * 1000

        print(
            f"{request.method} "
            f"{request.url.path} - "
            f"{process_time:.2f} ms"
        )

        return response

    except Exception as e:

        process_time = (
            time.time() - start_time
        ) * 1000

        print(
            f"{request.method} "
            f"{request.url.path} - "
            f"{process_time:.2f} ms - "
            f"ERROR: {e}"
        )

        raise


# ==========================================
# HOME ROUTE
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Welcome to TaskFlow API"
    }


# ==========================================
# INCLUDE ROUTERS
# ==========================================

app.include_router(
    users.router
)

app.include_router(
    projects.router
)

app.include_router(
    tasks.router
)

app.include_router(
    algorithms.router
)

app.include_router(
    quick_add.router
)