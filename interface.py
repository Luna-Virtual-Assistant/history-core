from abc import ABC, abstractmethod

class HistoryInterface(ABC):
    @abstractmethod
    def get_history(self):
        pass
    
    @abstractmethod
    def add_history(self, command: str, response: str) -> None:
        pass
    