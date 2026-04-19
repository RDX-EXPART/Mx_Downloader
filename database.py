from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URI, DB_NAME
from datetime import datetime

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

users_col = db["users"]
downloads_col = db["downloads"]


async def add_user(user_id: int, username: str = None, full_name: str = None):
    existing = await users_col.find_one({"user_id": user_id})
    if not existing:
        await users_col.insert_one({
            "user_id": user_id,
            "username": username,
            "full_name": full_name,
            "joined": datetime.utcnow(),
            "downloads": 0,
        })
    else:
        await users_col.update_one(
            {"user_id": user_id},
            {"$set": {"username": username, "full_name": full_name, "last_seen": datetime.utcnow()}}
        )


async def increment_download(user_id: int):
    await users_col.update_one({"user_id": user_id}, {"$inc": {"downloads": 1}})


async def log_download(user_id: int, title: str, url: str, quality: str):
    await downloads_col.insert_one({
        "user_id": user_id,
        "title": title,
        "url": url,
        "quality": quality,
        "timestamp": datetime.utcnow(),
    })


async def get_stats():
    total_users = await users_col.count_documents({})
    total_downloads = await downloads_col.count_documents({})
    return total_users, total_downloads


async def get_all_users():
    cursor = users_col.find({}, {"user_id": 1})
    return [doc["user_id"] async for doc in cursor]
