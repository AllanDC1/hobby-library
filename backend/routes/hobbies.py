from fastapi import APIRouter, HTTPException
from models.schemas import HobbyCreate, HobbyUpdate
from database.mongodb import (
    create_hobby, get_hobbies_by_user, get_hobby, update_hobby, delete_hobby
)
from database.redis_cache import (
    get_cached_hobbies, set_cached_hobbies, invalidate_hobbies_cache
)
from database.postgres import get_user

router = APIRouter(prefix="/api/users/{user_id}/hobbies", tags=["Hobbies"])


@router.post("")
async def add_hobby(user_id: str, payload: HobbyCreate):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    hobby_data = {
        "name": payload.name,
        "category": payload.category,
        **payload.fields
    }
    hobby = await create_hobby(user_id, hobby_data)
    await invalidate_hobbies_cache(user_id)
    return hobby


@router.get("")
async def list_hobbies(user_id: str):
    cached = await get_cached_hobbies(user_id)
    if cached is not None:
        return {"source": "cache", "hobbies": cached}

    hobbies = await get_hobbies_by_user(user_id)
    await set_cached_hobbies(user_id, hobbies)
    return {"source": "database", "hobbies": hobbies}


@router.get("/{hobby_id}")
async def get_hobby_detail(user_id: str, hobby_id: str):
    hobby = await get_hobby(hobby_id)
    if not hobby or hobby.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Hobby não encontrado")
    return hobby


@router.put("/{hobby_id}")
async def edit_hobby(user_id: str, hobby_id: str, payload: HobbyUpdate):
    existing = await get_hobby(hobby_id)
    if not existing or existing.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Hobby não encontrado")

    update_data = {}
    if payload.name is not None:
        update_data["name"] = payload.name
    if payload.category is not None:
        update_data["category"] = payload.category
    if payload.fields is not None:
        update_data.update(payload.fields)

    hobby = await update_hobby(hobby_id, update_data)
    await invalidate_hobbies_cache(user_id)
    return hobby


@router.delete("/{hobby_id}")
async def remove_hobby(user_id: str, hobby_id: str):
    existing = await get_hobby(hobby_id)
    if not existing or existing.get("user_id") != user_id:
        raise HTTPException(status_code=404, detail="Hobby não encontrado")

    await delete_hobby(hobby_id)
    await invalidate_hobbies_cache(user_id)
    return {"message": "Hobby removido com sucesso"}
