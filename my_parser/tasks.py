import asyncio
import logging

from broker_producer import CryptoProducer


class Scheduler:
    def __init__(self, producer: CryptoProducer):
        self.producer = producer
        self.logger = logging.getLogger(__name__)

    async def schedule_task(self):
        while True:
            self.logger.info('Sending all currency information')
            await self.producer.send_all_currency_info()
            await asyncio.sleep(60)