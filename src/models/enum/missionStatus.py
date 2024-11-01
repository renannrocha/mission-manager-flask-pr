from enum import Enum

class MissionStatus(Enum):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    ABORTED = "Aborted"
    CANCELLED = "Cancelled"