from database.db import get_connection
from models.contract import Contract

def _map(row) -> Contract:
    return Contract(*row)

def create(room_id: int, tenant_id: int, employee_id: int, start_date: str, end_date: str, cost: float) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Contract (room_id, tenant_id, employee_id, start_date, end_date, cost) VALUES (?, ?, ?, ?, ?, ?)",
        (room_id, tenant_id, employee_id, start_date, end_date, cost)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Contract]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contract_id, room_id, tenant_id, employee_id, start_date, end_date, cost FROM Contract")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(contract_id: int) -> Contract | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT contract_id, room_id, tenant_id, employee_id, start_date, end_date, cost FROM Contract WHERE contract_id = ?", (contract_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(contract_id: int, room_id: int, tenant_id: int, employee_id: int, start_date: str, end_date: str, cost: float) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Contract SET room_id = ?, tenant_id = ?, employee_id = ?, start_date = ?, end_date = ?, cost = ? WHERE contract_id = ?",
        (room_id, tenant_id, employee_id, start_date, end_date, cost, contract_id)
    )
    conn.commit()
    conn.close()

def delete(contract_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Contract WHERE contract_id = ?", (contract_id,))
    conn.commit()
    conn.close()