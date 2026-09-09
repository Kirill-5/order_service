import asyncio

import uvicorn
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from application.usecases.process_shipment_event import ProcessShipmentEventUsecase
from fastapi_app import create_app
from infrastructure.http.notification_client import HttpNotificationClient
from infrastructure.kafka.consumer import ShipmentEventConsumer
from infrastructure.kafka.producer import KafkaEventProducer
from infrastructure.persistence.outbox_worker import OutboxWorker
from infrastructure.persistence.uow import SQLAlchemyUnitOfWork
from settings import (
    DATABASE_URL,
    KAFKA_BOOTSTRAP_SERVERS,
    NOTIFICATIONS_SERVICE_API_KEY,
    NOTIFICATIONS_SERVICE_URL,
)

app = create_app()


async def main():
    engine = create_async_engine(DATABASE_URL)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    producer = KafkaEventProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await producer.start()

    worker = OutboxWorker(session_factory, producer)

    def usecase_factory():
        notification_client = HttpNotificationClient(
            base_url=NOTIFICATIONS_SERVICE_URL, api_key=NOTIFICATIONS_SERVICE_API_KEY
        )
        return ProcessShipmentEventUsecase(SQLAlchemyUnitOfWork(session_factory), notification_client)

    consumer = ShipmentEventConsumer(KAFKA_BOOTSTRAP_SERVERS, usecase_factory)
    await consumer.start()

    api_task = asyncio.create_task(
        uvicorn.Server(uvicorn.Config(app, host="0.0.0.0", port=8000)).serve()
    )
    worker_task = asyncio.create_task(worker.run())
    consumer_task = asyncio.create_task(consumer.run())

    await asyncio.gather(api_task, worker_task, consumer_task)


if __name__ == "__main__":
    asyncio.run(main())