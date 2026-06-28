from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class StockBalanceEntity:
    product_id: UUID
    location_id: UUID
    quantity: Decimal
