from database.db import get_connection
from models.tenant import Tenant

def _map(row) -> Tenant:
    return Tenant(*row)

def create(last_name: str, first_name: str, phone: str, login: str, password: str, middle_name: str | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Tenant (last_name, first_name, middle_name, phone, login, password) VALUES (?, ?, ?, ?, ?, ?)",
        (last_name, first_name, middle_name, phone, login, password)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Tenant]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tenant_id, last_name, first_name, middle_name, phone, login, password FROM Tenant")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(tenant_id: int) -> Tenant | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tenant_id, last_name, first_name, middle_name, phone, login, password FROM Tenant WHERE tenant_id = ?", (tenant_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_login(login: str) -> Tenant | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tenant_id, last_name, first_name, middle_name, phone, login, password FROM Tenant WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(tenant_id: int, last_name: str, first_name: str, phone: str, login: str, password: str, middle_name: str | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Tenant SET last_name = ?, first_name = ?, middle_name = ?, phone = ?, login = ?, password = ? WHERE tenant_id = ?",
        (last_name, first_name, middle_name, phone, login, password, tenant_id)
    )
    conn.commit()
    conn.close()

def delete(tenant_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tenant WHERE tenant_id = ?", (tenant_id,))
    conn.commit()
    conn.close()