from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from application.ports.order_repository import OrderRepositoryPort
from application.ports.unit_of_work import UnitOfWorkPort
from infrastructure.persistence.repository import SQLAlchemyOrderRepository



class SQLAlchemyUnitOfWork(UnitOfWorkPort):
    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def __aenter__(self):
        self.session = self.session_factory()
        self._order_repo = SQLAlchemyOrderRepository(self.session)
        return self


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        await self.session.close()


    @property
    def orders(self) -> OrderRepositoryPort:
        return self._order_repo


    async def commit(self) -> None:
        await self.session.commit()