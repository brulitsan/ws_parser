from fastapi import  FastAPI
import httpx

from broker_producer import send_currency_info
from database import save_data_to_mongo
from schemas import ParserSettings

app = FastAPI()
settings = ParserSettings()


class ParserBinance:
    async def get_binance_data(self, coin_data: str):
        coins = [coin_data]
        data = []
        async with httpx.AsyncClient() as client:
            for coin in coins:
                response = await client.get(url=settings.parser_url,
                                            params={"symbol": coin},
                                            )
                price_data = response.json()
                if 'highPrice' in price_data and 'lowPrice' in price_data and 'lastPrice' in price_data:
                    data.append({
                        'symbol': coin,
                        'highPrice': price_data['highPrice'],  # за 24 часа
                        'lowPrice': price_data['lowPrice'],  # за  24 часа
                        'lastPrice': price_data['lastPrice']  # Актуальная цена
                    })
                else:
                    print(f"Данные для {coin} не содержат 'highPrice', 'lowPrice' или 'lastPrice'.")
        await save_data_to_mongo(data)
        await send_currency_info(data)