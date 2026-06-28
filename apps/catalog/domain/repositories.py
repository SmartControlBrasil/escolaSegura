from abc import ABC, abstractmethod
class ProductRepository(ABC):
    @abstractmethod
    def find_active_by_sku(self, sku: str): ...
