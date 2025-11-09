from fastapi import FastAPI
from app.routers import outer_ear, middle_ear, input_signal
from fastapi.middleware.cors import CORSMiddleware

# API instance
app = FastAPI(
    title="Auditory System Models API",
    description="API with mathematical models of the human auditory system",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Local requests
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Routes
app.include_router(input_signal.router)
app.include_router(outer_ear.router)
app.include_router(middle_ear.router)
