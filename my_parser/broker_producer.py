import json

from aiokafka import AIOKafkaProducer


async def send_currency_info(data):
    producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
    await producer.start()
    try:
        for coin_data in data:
            await producer.send_and_wait("send_crypto_info", json.dumps(coin_data).encode())
    finally:
        await producer.stop()