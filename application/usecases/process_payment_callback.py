from datetime import UTC, datetime
from uuid import UUID, uuid4

import httpx

from application.ports.notification_client import NotificationClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import Order, OrderNotFoundError, OrderStatus


class ProcessPaymentCallbackUsecase:
    def __init__(self,
        uow: UnitOfWorkPort,
        notification_client: NotificationClientPort,):
        self.uow = uow
        self.notification_client = notification_client


    async def execute (self,
        order_id: UUID,
        payment_id: str,
        status: str,
        error_message: str | None
        )-> Order:

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
            order.updated_at = datetime.now(UTC)

            await uow.orders.update(order)
            await uow.commit()

            try:
                if order.status == OrderStatus.PAID:
                    await self.notification_client.send_notification(
                        message="Ваш заказ успешно оплачен и готов к отправке",
                        reference_id=str(order.id),
                        idempotency_key=str(uuid4())
                    )
                elif order.status == OrderStatus.CANCELLED:
                    await self.notification_client.send_notification(
                        message=f"Ваш заказ отменен. Причина: {error_message}",
                        reference_id=str(order.id),
                        idempotency_key=str(uuid4())
                    )
            except httpx.HTTPStatusError as e:
                print(f"Ошибка отправки уведомления пользователю: {e}")

            return order