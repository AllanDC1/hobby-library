import asyncio
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime, timezone
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["hobby_library"]
hobbies_collection = db["hobbies"]


async def create_hobby(user_id: str, hobby_data: dict) -> dict:
    document = {
        "user_id": user_id,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
        **hobby_data
    }
    
    def _insert():
        result = hobbies_collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return document
    
    result = await asyncio.to_thread(_insert)
    return _serialize(result)


async def get_hobbies_by_user(user_id: str) -> list[dict]:
    def _find():
        cursor = hobbies_collection.find({"user_id": user_id}).sort("created_at", -1)
        return [_serialize(doc) for doc in cursor]
    
    hobbies = await asyncio.to_thread(_find)
    return hobbies


async def get_hobby(hobby_id: str) -> dict | None:
    def _find_one():
        doc = hobbies_collection.find_one({"_id": ObjectId(hobby_id)})
        if doc:
            return _serialize(doc)
        return None
    
    return await asyncio.to_thread(_find_one)


async def update_hobby(hobby_id: str, hobby_data: dict) -> dict | None:
    hobby_data["updated_at"] = datetime.now(timezone.utc)
    
    def _update():
        result = hobbies_collection.find_one_and_update(
            {"_id": ObjectId(hobby_id)},
            {"$set": hobby_data},
            return_document=True
        )
        if result:
            return _serialize(result)
        return None
    
    return await asyncio.to_thread(_update)


async def delete_hobby(hobby_id: str) -> bool:
    def _delete():
        result = hobbies_collection.delete_one({"_id": ObjectId(hobby_id)})
        return result.deleted_count > 0
    
    return await asyncio.to_thread(_delete)


def _serialize(doc: dict) -> dict:
    serialized = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            serialized[key] = str(value)
        elif isinstance(value, datetime):
            serialized[key] = value.isoformat()
        else:
            serialized[key] = value
    return serialized
