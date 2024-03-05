import motor.motor_asyncio
from schemas import DbSettings


settings = DbSettings()


async def save_data_to_mongo(data: list):
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.db_name]
    collection = db[settings.collection_name]

    for item in data:
        item_without_id = {key: value for key, value in item.items() if key != "_id"}
        await collection.update_one({'symbol': item['symbol']}, {'$set': item_without_id}, upsert=True)


async def get_data_from_mongo():
    client = motor.motor_asyncio.AsyncIOMotorClient(settings.mongo_url)
    db = client[settings.db_name]
    collection = db[settings.collection_name]
    data = await collection.find({}).to_list(length=500)
    for item in data:
        item["_id"] = str(item["_id"])
    return data
