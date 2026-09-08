from datetime import datetime, timezone
from uuid import UUID
from uuid import uuid4

from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import Order, OrderNotFoundError, OrderStatus


class ProcessPaymentCallbackUsecase:
    def __init__(self, uow: UnitOfWorkPort):
        self.uow = uow


    async def execute (self, order_id: UUID, payment_id: str, status: str) -> Order:
        async with self.uow as uow:
            order = await uow.orders.get_by_id(order_id)

            if order is None:
                raise OrderNotFoundError(order_id)

            if order.status != OrderStatus.NEW:
                return order

            if status == "succeeded":
                order.status = OrderStatus.PAID
                payload = {
                    "event_type": "order.paid",
                    "order_id": str(order_id),
                    "item_id": order.item_id,
                    "quantity": order.quantity,
                    "idempotency_key": str(uuid4()),
                }
                await uow.outbox.add(topic="student_system-order.events", payload=payload)
            elif status == "failed":
                order.status = OrderStatus.CANCELLED

            order.payment_id = payment_id
            order.updated_at = datetime.now(timezone.utc)

            await uow.orders.update(order)
            await uow.commit()

            return order