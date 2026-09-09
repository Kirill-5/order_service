from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from application.usecases.create_order import CreateOrderUsecase
from application.usecases.get_order import GetOrderUsecase
from application.usecases.process_payment_callback import ProcessPaymentCallbackUsecase
from domain.order import InsufficientStockError, OrderNotFoundError
from presentation.api.dependencies import (
    get_create_order_usecase,
    get_get_order_usecase,
    get_process_payment_callback_usecase,
)
from presentation.api.schemas import (
    CreateOrderRequest,
    OrderResponse,
    PaymentCallbackRequest,
)

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


@router.post(
    "/api/orders/payment-callback",
    status_code=200,
)
async def payment_callback(
        callback: PaymentCallbackRequest,
        payment_callback_usecase: ProcessPaymentCallbackUsecase = Depends(get_process_payment_callback_usecase)
):
    await payment_callback_usecase.execute(
        order_id=callback.order_id,
        payment_id=callback.payment_id,
        status=callback.status,
        error_message=callback.error_message
    )

