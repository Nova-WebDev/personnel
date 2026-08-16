from abc import ABC, abstractmethod


class IGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass
