from dataclasses import dataclass
from typing import Optional
from datetime import datetime, UTC

@dataclass
class UserAnalytics:
    id: Optional[int] = None
    user_id: Optional[int] = None
    metric_name: str = ""
    metric_value: Optional[float] = None
    metric_data: Optional[dict] = None
    recorded_at: Optional[datetime] = None

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'user_id': self.user_id,
            'metric_name': self.metric_name,
            'metric_value': self.metric_value,
            'metric_data': self.metric_data,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }
