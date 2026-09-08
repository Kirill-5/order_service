from abc import ABC, abstractmethod

class OutboxRepositoryPort(ABC):
    @abstractmethod
    async def add(self, topic : str, payload : dict) -> None:
        pass


