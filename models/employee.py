from dataclasses import dataclass

@dataclass
class Employee:
    employee_id: int
    last_name: str
    first_name: str
    middle_name: str | None
    position: str
    login: str
    password: str