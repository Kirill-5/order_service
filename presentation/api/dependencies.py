from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from application.ports.catalog_client import CatalogClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from application.usecases.create_order import CreateOrderUsecase
from application.usecases.get_order import GetOrderUsecase
from infrastructure.http.catalog_client import HttpCatalogClient
from infrastructure.persistence.uow import SQLAlchemyUnitOfWork

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"

def get_session_factory():
    engine = create_async_engine(DATABASE_URL)
    return async_sessionmaker(engine, expire_on_commit=False)

def get_uow(session_factory = Depends(get_session_factory)) -> UnitOfWorkPort:
    return SQLAlchemyUnitOfWork(session_factory)


def get_catalog_client() -> CatalogClientPort:
    return HttpCatalogClient(base_url="http://catalog-service", api_key="api-key")


def get_create_order_usecase(uow = Depends(get_uow), catalog_client = Depends(get_catalog_client)) -> CreateOrderUsecase:
    return CreateOrderUsecase(uow, catalog_client)


def get_get_order_usecase(uow = Depends(get_uow)) -> GetOrderUsecase:
    return GetOrderUsecase(uow)