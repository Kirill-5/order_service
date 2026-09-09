from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from application.ports.catalog_client import CatalogClientPort
from application.ports.notification_client import NotificationClientPort
from application.ports.payment_client import PaymentClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from application.usecases.create_order import CreateOrderUsecase
from application.usecases.get_order import GetOrderUsecase
from application.usecases.process_payment_callback import ProcessPaymentCallbackUsecase
from infrastructure.http.catalog_client import HttpCatalogClient
from infrastructure.http.notification_client import HttpNotificationClient
from infrastructure.http.payment_client import HttpPaymentClient
from infrastructure.persistence.uow import SQLAlchemyUnitOfWork
from settings import (
    CATALOG_SERVICE_API_KEY,
    CATALOG_SERVICE_URL,
    DATABASE_URL,
    NOTIFICATIONS_SERVICE_API_KEY,
    NOTIFICATIONS_SERVICE_URL,
    PAYMENTS_SERVICE_API_KEY,
    PAYMENTS_SERVICE_URL,
)


def get_session_factory():
    engine = create_async_engine(DATABASE_URL)
    return async_sessionmaker(engine, expire_on_commit=False)


def get_uow(session_factory=Depends(get_session_factory)) -> UnitOfWorkPort:
    return SQLAlchemyUnitOfWork(session_factory)


def get_catalog_client() -> CatalogClientPort:
    return HttpCatalogClient(base_url=CATALOG_SERVICE_URL, api_key=CATALOG_SERVICE_API_KEY)


def get_payment_client() -> PaymentClientPort:
    return HttpPaymentClient(base_url=PAYMENTS_SERVICE_URL, api_key=PAYMENTS_SERVICE_API_KEY)


def get_notification_client() -> NotificationClientPort:
    return HttpNotificationClient(base_url=NOTIFICATIONS_SERVICE_URL, api_key=NOTIFICATIONS_SERVICE_API_KEY)


def get_create_order_usecase(
    uow=Depends(get_uow),
    catalog_client=Depends(get_catalog_client),
    payment_client=Depends(get_payment_client),
    notification_client=Depends(get_notification_client),
) -> CreateOrderUsecase:
    return CreateOrderUsecase(uow, catalog_client, payment_client, notification_client)


def get_get_order_usecase(uow=Depends(get_uow)) -> GetOrderUsecase:
    return GetOrderUsecase(uow)


def get_process_payment_callback_usecase(
    uow=Depends(get_uow),
    notification_client=Depends(get_notification_client),
) -> ProcessPaymentCallbackUsecase:
    return ProcessPaymentCallbackUsecase(uow, notification_client)