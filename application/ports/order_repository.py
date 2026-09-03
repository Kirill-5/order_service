from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.order import Order


class OrderRepositoryPort(ABC):
    @abstractmethod
    async def add(self, order: Order) -> None:
        pass

    @abstractmethod
    async def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    async def get_by_idempotency_key(self, key: str) -> Optional[Order]:
        pass