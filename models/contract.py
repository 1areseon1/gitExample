from dataclasses import dataclass

@dataclass
class Contract:
    contract_id: int
    room_id: int
    tenant_id: int
    employee_id: int
    start_date: str
    end_date: str
    cost: float