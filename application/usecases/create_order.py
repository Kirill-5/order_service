from datetime import datetime, timezone
from uuid import UUID, uuid4

from application.ports import catalog_client
from application.ports.catalog_client import CatalogClientPort
from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import InsufficientStockError, Order, OrderStatus



class CreateOrderUsecase:
    def __init__(self, uow: UnitOfWorkPort, catalog_client: CatalogClientPort):
        self.uow = uow
        self.catalog_client = catalog_client


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

            await uow.orders.add(new_order)
            await uow.commit()

            return new_order
        