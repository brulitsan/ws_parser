import fastapi

from my_parser.database import get_data_from_mongo
from my_parser.parser import ParserBinance


async def get_coins():
    parser = ParserBinance()
    await parser.get_binance_data()
    return await get_data_from_mongo()
