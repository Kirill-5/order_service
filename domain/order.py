from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID

class OrderStatus(Enum):
    NEW = 'NEW'
    PAID = 'PAID'
    SHIPPED = 'SHIPPED'
    CANCELLED = 'CANCELLED'

@dataclass
class Order:
    id: UUID
    user_id: str
    item_id: str
    quantity: int
    status: OrderStatus
    idempotency_key: str
    created_at: datetime
    updated_at: datetime



class InsufficientStockError(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Insufficient stock for {item_id}")


class OrderNotFoundError(Exception):
    def __init__(self, order_id: str):
        self.order_id = order_id
        super().__init__(f"Order {order_id} not found")


class ItemNotFoundError(Exception):
    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")