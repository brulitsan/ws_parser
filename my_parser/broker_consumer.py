import asyncio
import os

from aiokafka import AIOKafkaConsumer

from broker_producer import CryptoProducer
from database import MongoManager
from parser import ParserBinance
import logging

from schemas import DbSettings
from tasks import Scheduler


class ConsumerBinance:
    def __init__(self, parser: ParserBinance, settings: DbSettings):
        self.parser = parser
        self.queue = asyncio.Queue()
        self.logger = logging.getLogger(__name__)
        self.producer = CryptoProducer(settings=settings)
        self.database = MongoManager(settings=settings)

    async def consume_messages(self):
        consumer = AIOKafkaConsumer(
            'take_crypto_requests',
            bootstrap_servers=os.environ.get('KAFKA_BROKER_PATH'),
            group_id='group_id',
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        await consumer.start()
        self.logger.info('Consumer started')
        async for msg in consumer:
            self.logger.info('Message received')
            await self.queue.put(msg.value)
            self.logger.info('Message putted')
        await consumer.stop()

    async def process_messages(self):
        while True:
            coin_data_bite = await self.queue.get()
            coin_data = coin_data_bite.decode()
            data = await self.parser.get_binance_data(coin_data)
            await self.database.save_data_to_mongo(data)
            await self.producer.send_currency_info(data)

    async def run(self):
        tasks = [
            asyncio.ensure_future(self.consume_messages()),
            asyncio.ensure_future(self.process_messages()),
        ]
        await asyncio.gather(*tasks)


async def main():
    parser = ParserBinance()
    settings = DbSettings()
    consumer = ConsumerBinance(parser, settings)
    producer = CryptoProducer(settings=settings)
    scheduler = Scheduler(producer)
    tasks = [
        asyncio.create_task(scheduler.schedule_task()),
        asyncio.ensure_future(consumer.run()),
    ]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
