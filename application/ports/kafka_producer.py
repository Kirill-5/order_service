from abc import ABC, abstractmethod


class KafkaProducerPort(ABC):
    @abstractmethod
    async def send(self, topic: str, key: str, value: dict) -> None:
        pass