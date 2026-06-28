from abc import ABC, abstractmethod
from typing import Any

class SystemSettingRepository(ABC):
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any: ...

    @abstractmethod
    def set(self, key: str, value: Any, description: str = '') -> Any: ...
