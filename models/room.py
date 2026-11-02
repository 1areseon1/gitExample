from dataclasses import dataclass

@dataclass
class Room:
    room_id: int
    number: str
    type: str
    area: float
    status: str