import json
from uuid import UUID

from aiokafka import AIOKafkaConsumer


class ShipmentEventConsumer:
    def __init__(self, bootstrap_servers: str, usecase_factory):
        self.usecase_factory = usecase_factory
        self.consumer = AIOKafkaConsumer(
            "student_system-shipment.events",
            bootstrap_servers=bootstrap_servers,
            group_id="order-service",
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def run(self):
        async for message in self.consumer:
            data = json.loads(message.value)
            usecase = self.usecase_factory()
            await usecase.execute(
                event_type=data["event_type"],
                order_id=UUID(data["order_id"]),
                reason=data.get("reason"),
            )