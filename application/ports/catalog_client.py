from abc import ABC, abstractmethod
from dataclasses import dataclass



@dataclass
class CatalogItemDto:
    id: str
    name: str
    price: str
    available_qty: int
    created_at: str



class CatalogClientPort(ABC):
    @abstractmethod
    async def get_item(self, item_id: str) -> CatalogItemDto:
        pass