from dataclasses import dataclass

@dataclass
class Tenant:
    tenant_id: int
    last_name: str
    first_name: str
    middle_name: str | None
    phone: str
    login: str
    password: str