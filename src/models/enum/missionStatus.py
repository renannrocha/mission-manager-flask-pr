from enum import Enum

class MissionStatus(Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    ABORTED = "ABORTED"
    CANCELLED = "CANCELLED"

    @classmethod
    def is_valid(cls, value):
        return value.upper() in [status.value for status in cls]