from dataclasses import dataclass
from uuid import UUID

@dataclass(frozen=True)
class UserEntity:
    id: UUID
    username: str
    email: str
    role: str
