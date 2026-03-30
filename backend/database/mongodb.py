from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from datetime import datetime, timezone
from config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["hobby_library"]
hobbies_collection = db["hobbies"]


async def create_hobby(user_id: str, hobby_data: dict) -> dict:
    document = {
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        **hobby_data
    }
    result = await hobbies_collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    return _serialize(document)


async def get_hobbies_by_user(user_id: str) -> list[dict]:
    cursor = hobbies_collection.find({"user_id": user_id}).sort("created_at", -1)
    hobbies = []
    async for doc in cursor:
        hobbies.append(_serialize(doc))
    return hobbies


async def get_hobby(hobby_id: str) -> dict | None:
    doc = await hobbies_collection.find_one({"_id": ObjectId(hobby_id)})
    if doc:
        return _serialize(doc)
    return None


async def update_hobby(hobby_id: str, hobby_data: dict) -> dict | None:
    hobby_data["updated_at"] = datetime.now(timezone.utc)
    result = await hobbies_collection.find_one_and_update(
        {"_id": ObjectId(hobby_id)},
        {"$set": hobby_data},
        return_document=True
    )
    if result:
        return _serialize(result)
    return None


async def delete_hobby(hobby_id: str) -> bool:
    result = await hobbies_collection.delete_one({"_id": ObjectId(hobby_id)})
    return result.deleted_count > 0


def _serialize(doc: dict) -> dict:
    """Converte ObjectId e datetime para strings serializáveis."""
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized
