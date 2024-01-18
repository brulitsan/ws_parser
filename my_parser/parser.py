import requests
from fastapi import BackgroundTasks, FastAPI
import httpx
from .database import save_data_to_mongo

app = FastAPI()

@app.on_event("startup")
async def run_parser():
    background_tasks = BackgroundTasks()
    parser = ParserBinance()
    background_tasks.add_task(parser.get_binance_data)


class ParserBinance:
    async def get_binance_data(self):
        coins = ["BTCUSDT",
                 "ETHUSDT",
                 "LTCUSDT",
                 "XRPUSDT",
                 "BCHUSDT",
                 "EOSUSDT",
                 "ZECUSDT",
                 "TRXUSDT",
                 "ADAUSDT",
                 "XLMUSDT"]
        data = []

        async with httpx.AsyncClient() as client:
            for coin in coins:
                response = await client.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin}")
                data.append(response.json())
        await save_data_to_mongo(data)
