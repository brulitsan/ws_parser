import json
import logging
import os

from aiokafka import AIOKafkaProducer

from database import MongoManager
from parser import ParserBinance
from schemas import DbSettings


class CryptoProducer:
    def __init__(self, settings: DbSettings):
        config = {
            'bootstrap_servers': os.environ.get('KAFKA_BROKER_PATH')
        }
        self.producer = AIOKafkaProducer(**config)
        self.logger = logging.getLogger(__name__)
        self.parser = ParserBinance()
        self.db = MongoManager(settings)
        self.running = True

    async def send_all_currency_info(self) -> None:
        await self.producer.start()
        mongo_manager = self.db
        symbols = await mongo_manager.get_symbols_from_mongo()
        coin_data_list = []
        for symbol in symbols:
            coin_data = await self.parser.get_binance_data(symbol)
            coin_data_list.append(coin_data)
        if coin_data_list:
            await self.producer.send_and_wait('send_crypto_info', json.dumps(coin_data_list).encode())
            self.logger.info('Batch of messages submitted')

    async def send_currency_info(self, data: list[dict[str]]) -> None:
        await self.producer.start()
        try:
            coin_data_list = []
            for coin_data in data:
                coin_data_list.append(coin_data)
            await self.producer.send_and_wait('send_crypto_info', json.dumps(coin_data_list).encode())
            self.logger.info('Message submitted')
        except KeyError as error:
            self.logger.error(f"Key error: {error}")
        except ValueError as error:
            self.logger.error(f"Value error: {error}")
        except Exception as error:
            self.logger.error(f"Unexpected error: {error}")
        finally:
            if not self.running:
                await self.producer.stop()
