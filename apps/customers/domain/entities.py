from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class CustomerEntity:
    id: UUID
    name: str
    document: str = ''
