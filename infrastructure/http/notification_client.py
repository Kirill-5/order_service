import httpx

from application.ports.notification_client import NotificationClientPort


class HttpNotificationClient(NotificationClientPort):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()

    async def send_notification(self, message: str, reference_id: str, idempotency_key: str) -> None:
        url = f"{self.base_url}/api/notifications"
        headers = {"X-Api-Key": self.api_key}

        response = await self.client.post(
        url,
        headers=headers,
        json={
            "message": message,
            "reference_id": reference_id,
            "idempotency_key": idempotency_key,
        })

        response.raise_for_status()