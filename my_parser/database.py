import motor.motor_asyncio
from schemas import DbSettings


class MongoManager:
    def __init__(self, settings: DbSettings):
        self.settings = settings

    async def save_data_to_mongo(self, data: list[dict[str]]):
        client = motor.motor_asyncio.AsyncIOMotorClient(self.settings.mongo_url)
        db = client[self.settings.db_name]
        collection = db[self.settings.collection_name]

        for item in data:
            item_without_id = {key: value for key, value in item.items() if key != "_id"}
            await collection.update_one({'symbol': item['symbol']}, {'$set': item_without_id}, upsert=True)

    async def get_data_from_mongo(self):
        client = motor.motor_asyncio.AsyncIOMotorClient(self.settings.mongo_url)
        db = client[self.settings.db_name]
        collection = db[self.settings.collection_name]
        data = await collection.find({}).to_list(length=500)
        for item in data:
            item["_id"] = str(item["_id"])
        return data

    async def get_symbols_from_mongo(self):
        data = await self.get_data_from_mongo()
        symbols = [item["symbol"] for item in data]
        return symbols
