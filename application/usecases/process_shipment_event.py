from uuid import UUID, uuid4

import httpx

from application.ports.notification_client import NotificationClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import OrderNotFoundError, OrderStatus


class ProcessShipmentEventUsecase:
    def __init__(self, uow: UnitOfWorkPort, notification_client: NotificationClientPort):
        self.uow = uow
        self.notification_client = notification_client

    async def execute(self, event_type: str, order_id: UUID, reason: str | None = None) -> None:
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

            try:
                if order.status == OrderStatus.SHIPPED:
                    await self.notification_client.send_notification(
                        message="Ваш заказ отправлен в доставку",
                        reference_id=str(order.id),
                        idempotency_key=str(uuid4()),
                    )
                elif order.status == OrderStatus.CANCELLED:
                    await self.notification_client.send_notification(
                        message=f"Ваш заказ отменен. Причина: {reason}",
                        reference_id=str(order.id),
                        idempotency_key=str(uuid4()),
                    )
            except httpx.HTTPStatusError:
                print("Ошибка отправки уведомления пользователю")

            return