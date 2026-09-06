from abc import ABC, abstractmethod


class IEventPublisher(ABC):
    @abstractmethod
    async def publish(
        self,
        event: str,
        scope: str,
        data: dict,
        meta: dict | None = None,
        targets: list[str] | None = None,
    ) -> None:
        pass