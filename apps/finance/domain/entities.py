from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class ReceivableEntity:
    id: UUID
    description: str
    amount: Decimal
    status: str
