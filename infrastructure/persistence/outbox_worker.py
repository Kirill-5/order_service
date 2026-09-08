import asyncio

from sqlalchemy import select

from application.ports.kafka_producer import KafkaProducerPort
from infrastructure.persistence.models import OutboxModel


class OutboxWorker:
    def __init__(self, session_factory, producer: KafkaProducerPort):
        self.session_factory = session_factory
        self.producer = producer

    async def run(self):
        while True:
            await self._process_batch()
            await asyncio.sleep(2)


    async def _process_batch(self):
        async with self.session_factory() as session:
            stmt = (
                select(OutboxModel)
                .where(OutboxModel.is_sent == False)
                .limit(10)
                .with_for_update(skip_locked=True)
            )
            result = await session.execute(stmt)
            records = result.scalars().all()

            for record in records:
                await self.producer.send(topic=record.topic, key=str(record.id), value=record.payload)
                record.is_sent = True
                await session.commit()