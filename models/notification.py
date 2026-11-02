from dataclasses import dataclass

@dataclass
class Notification:
    notification_id: int
    room_id: int
    employee_id: int
    description: str