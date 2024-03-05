import json
import os

from aiokafka import AIOKafkaProducer


async def send_currency_info(data: dict) -> None:
    producer = AIOKafkaProducer(bootstrap_servers=os.environ.get('KAFKA_BROKER_PATH'))  # add logs
    await producer.start()
    try:
        coin_data_list = []
        for coin_data in data:
            coin_data_list.append(coin_data)
        await producer.send_and_wait('send_crypto_info', json.dumps(coin_data_list).encode())
    finally:
        await producer.stop()
