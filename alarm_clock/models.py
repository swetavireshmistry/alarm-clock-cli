import datetime
import uuid
from dataclasses import dataclass, field

@dataclass
class Alarm:
    """Represents a single alarm."""
    time: str  # Format: "HH:MM"
    label: str = "Alarm"
    is_active: bool = True
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    
    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "time": self.time,
            "label": self.label,
            "is_active": self.is_active
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Alarm":
        """Deserialize from dictionary."""
        return cls(
            id=data.get("id"),
            time=data["time"],
            label=data.get("label", "Alarm"),
            is_active=data.get("is_active", True)
        )
