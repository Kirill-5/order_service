from abc import ABC, abstractmethod


class InboxRepositoryPort(ABC):
    @abstractmethod
    async def is_processed(self, event_key: str) -> bool:
        pass


    @abstractmethod
    async def mark_processed(self, event_key: str) -> None:
        pass