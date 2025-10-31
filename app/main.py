from fastapi import FastAPI
from app.routers import outer_ear, middle_ear

# Cria a instância principal da API
app = FastAPI(
    title="Auditory System Models API",
    description="API with mathematical models of the human auditory system",
    version="0.1.0"
)

# Registra os módulos de rotas
app.include_router(outer_ear.router)
app.include_router(middle_ear.router)
