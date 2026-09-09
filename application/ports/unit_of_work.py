from abc import ABC, abstractmethod

from application.ports.inbox_repository import InboxRepositoryPort
from application.ports.order_repository import OrderRepositoryPort
from application.ports.outbox_repository import OutboxRepositoryPort


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

    @property
    @abstractmethod
    def outbox(self) -> OutboxRepositoryPort:
        pass


    @property
    @abstractmethod
    def inbox(self) -> InboxRepositoryPort:
        pass