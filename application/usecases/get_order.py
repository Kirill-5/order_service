from uuid import UUID


from application.ports.unit_of_work import UnitOfWorkPort
from domain.order import OrderNotFoundError, Order



class GetOrderUsecase:
    def __init__(self, uow: UnitOfWorkPort):
        self.uow = uow


    async def execute(self, order_id: UUID) -> Order:
        async with self.uow as uow:
            order = await uow.orders.get_by_id(order_id)

            if order is not None:
                return order
            raise OrderNotFoundError(order_id)