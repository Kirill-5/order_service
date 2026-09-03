import httpx

from application.ports.catalog_client import CatalogClientPort, CatalogItemDto
from domain.order import ItemNotFoundError


class HttpCatalogClient(CatalogClientPort):
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.client = httpx.AsyncClient()


    async def get_item(self, item_id: str) -> CatalogItemDto:
        url = f"{self.base_url}/api/catalog/items/{item_id}"
        headers = {"X-Api-Key": self.api_key}

        response = await self.client.get(url, headers=headers)

        if response.status_code == 404:
            raise ItemNotFoundError(item_id)

        response.raise_for_status()

        data = response.json()

        return CatalogItemDto(
            id=data["id"],
            name=data["name"],
            price=data["price"],
            available_qty=data["available_qty"],
            created_at=data["created_at"],
        )