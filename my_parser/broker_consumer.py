import asyncio
import os

from aiokafka import AIOKafkaConsumer

from my_parser import parser


async def take_info_about_requested_data():  # стринг валюты, которой надо найти инфу
    consumer = AIOKafkaConsumer(
        'take_crypto_requests',
        bootstrap_servers=os.environ.get('KAFKA_BROKER_PATH'))  # сделать логгирование
    await consumer.start()
    try:
        async for msg in consumer:
            coin_data = msg.value.decode()
            parser_binance = parser.ParserBinance()
            await parser_binance.get_binance_data(coin_data)
    finally:
        await consumer.stop()


asyncio.run(take_info_about_requested_data())