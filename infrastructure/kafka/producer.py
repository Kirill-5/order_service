import json

from aiokafka import AIOKafkaProducer

from application.ports.kafka_producer import KafkaProducerPort


class KafkaEventProducer(KafkaProducerPort):
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)


    async def start(self):
       await self.producer.start()


    async def stop(self):
        await self.producer.stop()


    async def send(self, topic: str, key: str, value: dict) -> None:
        json_message = json.dumps(value).encode()
        key = key.encode()
        await self.producer.send_and_wait(topic=topic, key=key, value=json_message)