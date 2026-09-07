import httpx


from application.ports.payment_client import  PaymentDto, PaymentClientPort


class HttpPaymentClient(PaymentClientPort):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()


    async def create_payment(self,
        order_id : str,
        amount : str,
        callback_url : str,
        idempotency_key : str
    ) -> PaymentDto:
        url = f"{self.base_url}/api/payments"
        headers = {"X-Api-Key": self.api_key}

        response = await self.client.post(
            url,
            headers=headers,
            json={
                "order_id": order_id,
                "amount": amount,
                "callback_url": callback_url,
                "idempotency_key": idempotency_key
            })

        response.raise_for_status()

        return PaymentDto(id= response.json()["id"], status=response.json()["status"])