from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PaymentDto:
    id: str
    status: str


class PaymentClientPort(ABC):
    @abstractmethod
    async def create_payment(
            self,
            order_id: str,
            amount: str,
            callback_url: str,
            idempotency_key: str
    ) -> PaymentDto:
        pass