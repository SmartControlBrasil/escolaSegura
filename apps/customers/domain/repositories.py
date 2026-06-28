from abc import ABC, abstractmethod
class CustomerRepository(ABC):
    @abstractmethod
    def find_by_document(self, document: str): ...
