from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.order_repository import OrderRepositoryPort
from domain.order import Order
from infrastructure.persistence.models import OrderModel


class SQLAlchemyOrderRepository(OrderRepositoryPort):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, order: Order) -> None:
        model = OrderModel(
            id=order.id,
            user_id=order.user_id,
            item_id=order.item_id,
            quantity=order.quantity,
            status=order.status,
            idempotency_key=order.idempotency_key,
            created_at=order.created_at,
            updated_at=order.updated_at,
        )
        self.session.add(model)

    async def get_by_id(self, order_id) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.id == order_id)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    async def get_by_idempotency_key(self, key: str) -> Order | None:
        stmt = select(OrderModel).where(OrderModel.idempotency_key == key)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_domain(model)

    def _to_domain(self, model: OrderModel) -> Order:
        return Order(
            id=model.id,
            user_id=model.user_id,
            item_id=model.item_id,
            quantity=model.quantity,
            status=model.status,
            idempotency_key=model.idempotency_key,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )