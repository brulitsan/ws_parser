import motor.motor_asyncio
import os


async def save_data_to_mongo(data: list):
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    collection = db[os.environ.get('COLLECTION_NAME')]
    for item in data:
        item_without_id = {key: value for key, value in item.items() if key != "_id"}
        await collection.update_one({'symbol': item['symbol']}, {'$set': item_without_id}, upsert=True)


async def get_data_from_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGO_URL'))
    db = client[os.environ.get('DB_NAME')]
    collection = db[os.environ.get('COLLECTION_NAME')]
    data = await collection.find({}).to_list(length=500)
    for item in data:
        item["_id"] = str(item["_id"])
    return data