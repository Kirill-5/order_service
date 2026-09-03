from http import HTTPStatus

from fastapi import APIRouter, Depends

from starlette.responses import JSONResponse

from uuid import UUID
from application.usecases.create_order import CreateOrderUsecase
from application.usecases.get_order import GetOrderUsecase
from domain.order import OrderNotFoundError, InsufficientStockError
from presentation.api.schemas import OrderResponse, CreateOrderRequest
from presentation.api.dependencies import get_create_order_usecase, get_get_order_usecase

router = APIRouter()


@router.post(
    "/api/orders",
        status_code=201,
        response_model=OrderResponse)

async def create_order(
        order: CreateOrderRequest,
        create_order_usecase: CreateOrderUsecase = Depends(get_create_order_usecase)
):
    try:
        return await create_order_usecase.execute(
            user_id=order.user_id,
            item_id=order.item_id,
            quantity=order.quantity,
            idempotency_key=order.idempotency_key
        )
    except InsufficientStockError as e:
        return JSONResponse(
            content = {"message": str(e)},
            status_code = HTTPStatus.BAD_REQUEST,
        )



@router.get(
    "/api/orders/{order_id}",
    response_model=OrderResponse
)

async def get_order(
        order_id: UUID,
        get_order_usecase: GetOrderUsecase = Depends(get_get_order_usecase)
):
    try:
        return await get_order_usecase.execute(
            order_id=order_id,
        )
    except OrderNotFoundError as e:
        return JSONResponse(
            content = {"message": str(e)},
            status_code = HTTPStatus.NOT_FOUND,
        )