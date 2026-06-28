from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class OrganizationEntity:
    id: UUID
    name: str
    document: str = ''
