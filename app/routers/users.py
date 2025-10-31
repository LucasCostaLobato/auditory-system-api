from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

# Lista de usuários simulada em memória
users_db = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"}
]

@router.get("/")
async def list_users():
    return users_db

@router.get("/{user_id}")
async def get_user(user_id: int):
    for user in users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")