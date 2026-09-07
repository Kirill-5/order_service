from datetime import datetime, timezone
from uuid import UUID, uuid4
from decimal import Decimal

import httpx


from application.ports.catalog_client import CatalogClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from application.ports.payment_client import PaymentClientPort
from domain.order import InsufficientStockError, Order, OrderStatus
from settings import ORDER_SERVICE_CALLBACK_URL


class CreateOrderUsecase:
    def __init__(self, uow: UnitOfWorkPort, catalog_client: CatalogClientPort, payment_client: PaymentClientPort):
        self.uow = uow
        self.catalog_client = catalog_client
        self.payment_client = payment_client


    async def execute(self, user_id: str, item_id: str, quantity: int, idempotency_key: str) -> Order:
        async with self.uow as uow:

            existing_order = await uow.orders.get_by_idempotency_key(idempotency_key)
            if existing_order is not None:
                return existing_order
            item = await self.catalog_client.get_item(item_id)

            if not item.available_qty >= quantity:
                raise InsufficientStockError(item_id)

            new_order = Order(
                id = uuid4(),
                user_id = user_id,
                item_id = item_id,
                quantity = quantity,
                status = OrderStatus.NEW,
                idempotency_key = idempotency_key,
                created_at = datetime.now(timezone.utc),
                updated_at = datetime.now(timezone.utc),
            )

            try:
                payment = await self.payment_client.create_payment(
                    order_id=str(new_order.id),
                    amount = str(Decimal(item.price)* quantity),
                    callback_url=ORDER_SERVICE_CALLBACK_URL,
                    idempotency_key=idempotency_key,
                )
                new_order.payment_id = payment.id
            except httpx.HTTPStatusError:
                new_order.status = OrderStatus.CANCELLED



            await uow.orders.add(new_order)
            await uow.commit()

            return new_order
