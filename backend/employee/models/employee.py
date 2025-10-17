from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime, UTC

@dataclass
class Employee:
    id: Optional[int] = None
    name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip: str
    country: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))