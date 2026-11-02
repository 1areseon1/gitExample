from database.db import get_connection
from models.tenant import Tenant

def _map(row) -> Tenant:
    return Tenant(*row)

def create(last_name: str, first_name: str, middle_name: str | None, phone: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Tenant (last_name, first_name, middle_name, phone) VALUES (?, ?, ?, ?)",
        (last_name, first_name, middle_name, phone)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Tenant]:
    conn = get_connection()
    cur = conn.cursor()
    # ВАЖНО: порядок колонок должен совпадать с моделью (ID, Фамилия, Имя, Отчество, Телефон)
    cur.execute("SELECT tenant_id, last_name, first_name, middle_name, phone FROM Tenant")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(tenant_id: int) -> Tenant | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tenant_id, last_name, first_name, middle_name, phone FROM Tenant WHERE tenant_id = ?", (tenant_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(tenant_id: int, last_name: str, first_name: str, middle_name: str | None, phone: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Tenant SET last_name = ?, first_name = ?, middle_name = ?, phone = ? WHERE tenant_id = ?",
        (last_name, first_name, middle_name, phone, tenant_id)
    )
    conn.commit()
    conn.close()

def delete(tenant_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Tenant WHERE tenant_id = ?", (tenant_id,))
    conn.commit()
    conn.close()