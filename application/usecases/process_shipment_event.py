from uuid import UUID

from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import Order, OrderNotFoundError, OrderStatus


class ProcessShipmentEventUsecase:
    def __init__(self, uow: UnitOfWorkPort):
        self.uow = uow

    async def execute(self, event_type: str, order_id: UUID) -> None:
        async with self.uow as uow:
            event_key = f"{event_type}:{order_id}"

            if await uow.inbox.is_processed(event_key):
                return

            order = await uow.orders.get_by_id(order_id)
            if order is None:
                raise OrderNotFoundError(order_id)

            if event_type == "order.shipped":
                order.status = OrderStatus.SHIPPED

            elif event_type == "order.cancelled":
                order.status = OrderStatus.CANCELLED

            await uow.orders.update(order)
            await uow.inbox.mark_processed(event_key)
            await uow.commit()