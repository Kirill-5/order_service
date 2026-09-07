from datetime import datetime, timezone
from uuid import UUID

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
            elif status == "failed":
                order.status = OrderStatus.CANCELLED

            order.payment_id = payment_id
            order.updated_at = datetime.now(timezone.utc)

            await uow.orders.update(order)
            await uow.commit()

            return order