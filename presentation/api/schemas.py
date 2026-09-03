from datetime import datetime

from pydantic import BaseModel
from uuid import UUID

from domain.order import OrderStatus


class CreateOrderRequest(BaseModel):
    user_id: str
    quantity: int
    item_id: str
    idempotency_key: str


class OrderResponse(BaseModel):
    id: UUID
    user_id: str
    quantity: int
    item_id: str
    status: OrderStatus
    created_at: datetime
    updated_at: datetime