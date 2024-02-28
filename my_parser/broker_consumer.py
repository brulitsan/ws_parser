import asyncio
import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from my_parser import parser


async def send_currency_info(data):
    producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        for coin_data in data:
            await producer.send_and_wait("send_crypto_info", json.dumps(coin_data).encode())
    finally:
        await producer.stop()


async def take_info_about_requested_data():  # стринг валюты, которой надо найти инфу
    consumer = AIOKafkaConsumer(
        'take_crypto_requests',
        bootstrap_servers='kafka:9092')
    await consumer.start()
    try:
        async for msg in consumer:
            coin_data = msg.value.decode('utf-8')
            parser_binance = parser.ParserBinance()
            await parser_binance.get_binance_data(coin_data)
    finally:
        await consumer.stop()


asyncio.run(take_info_about_requested_data())