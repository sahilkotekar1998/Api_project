from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from bson.objectid import ObjectId

MONGO_URL = "mongodb+srv://Hariomsimform123:w6dLtUqi7Bim9Jxl@cluster0.ealz30c.mongodb.net/"
MONGO_DB_NAME = "user_profile"

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]
fs = AsyncIOMotorGridFSBucket(db)

async def save_profile_picture(email: str, file_content: bytes):
    user_profile = db.profile_pictures
    picture_id = await fs.upload_from_stream(email, file_content)
    await user_profile.insert_one({"email": email, "picture_id": picture_id})
