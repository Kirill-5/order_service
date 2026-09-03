from abc import ABC, abstractmethod

from application.ports.order_repository import OrderRepositoryPort

class UnitOfWorkPort(ABC):
    @abstractmethod
    async def __aenter__(self) -> "UnitOfWorkPort":
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @property
    @abstractmethod
    def orders(self) -> OrderRepositoryPort:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass