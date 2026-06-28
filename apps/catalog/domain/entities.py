from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID

@dataclass(frozen=True)
class ProductEntity:
    id: UUID
    name: str
    sku: str
    sale_price: Decimal
