from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class SalesOrderEntity:
    id: UUID
    customer_id: UUID
    total_amount: Decimal
    status: str
