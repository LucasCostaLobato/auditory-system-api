from fastapi import FastAPI
from app.routers import users

# Cria a instância principal da API
app = FastAPI(
    title="Minha API com FastAPI",
    description="Exemplo inicial de estrutura organizada",
    version="0.1.0"
)

# Registra os módulos de rotas
app.include_router(users.router)

# Endpoint simples de teste
@app.get("/")
async def root():
    return {"message": "API funcionando com sucesso 🚀"}