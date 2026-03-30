from fastapi import APIRouter, HTTPException
from models.schemas import UserCreate
from database.postgres import create_user, get_user, get_user_by_email, list_users

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("")
def register_user(payload: UserCreate):
    existing = get_user_by_email(payload.email)
    if existing:
        return existing  # retorna o usuário já existente
    user = create_user(payload.username, payload.email)
    return user


@router.get("")
def get_all_users():
    return list_users()


@router.get("/{user_id}")
def get_user_detail(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user
