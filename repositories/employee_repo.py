from database.db import get_connection
from models.employee import Employee

def _map(row) -> Employee:
    return Employee(*row)

def create(last_name: str, first_name: str, position: str, login: str, password: str, middle_name: str | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Employee (last_name, first_name, middle_name, position, login, password) VALUES (?, ?, ?, ?, ?, ?)",
        (last_name, first_name, middle_name, position, login, password)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Employee]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, last_name, first_name, middle_name, position, login, password FROM Employee")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(employee_id: int) -> Employee | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, last_name, first_name, middle_name, position, login, password FROM Employee WHERE employee_id = ?", (employee_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def get_by_login(login: str) -> Employee | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT employee_id, last_name, first_name, middle_name, position, login, password FROM Employee WHERE login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(employee_id: int, last_name: str, first_name: str, position: str, login: str, password: str, middle_name: str | None = None) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Employee SET last_name = ?, first_name = ?, middle_name = ?, position = ?, login = ?, password = ? WHERE employee_id = ?",
        (last_name, first_name, middle_name, position, login, password, employee_id)
    )
    conn.commit()
    conn.close()

def delete(employee_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Employee WHERE employee_id = ?", (employee_id,))
    conn.commit()
    conn.close()