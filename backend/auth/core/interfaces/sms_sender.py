from abc import ABC, abstractmethod


class ISmsSender(ABC):
    @abstractmethod
    async def send(self, phone_number: str, code: str):
        pass
