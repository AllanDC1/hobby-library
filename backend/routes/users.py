from fastapi import APIRouter, HTTPException
from models.schemas import UserCreate
from database.postgres import create_user, get_user, get_user_by_email

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("")
def register_user(payload: UserCreate):
    existing = get_user_by_email(payload.email)
    if existing:
        if existing["username"] != payload.username:
            raise HTTPException(
                status_code=401,
                detail="Conta já registrada com esse email."
            )
        return existing
    user = create_user(payload.username, payload.email)
    return user
