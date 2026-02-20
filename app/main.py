import os
from fastapi import FastAPI
from app.routers import outer_ear, middle_ear, input_signal, inner_ear, fundamentals
from fastapi.middleware.cors import CORSMiddleware

# API instance
app = FastAPI(
    title="Auditory System Models API",
    description="API with mathematical models of the human auditory system",
    version="0.1.0"
)

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in _raw_origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Routes
app.include_router(input_signal.router)
app.include_router(outer_ear.router)
app.include_router(middle_ear.router)
app.include_router(inner_ear.router)
app.include_router(fundamentals.router)
