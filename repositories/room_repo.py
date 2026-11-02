from database.db import get_connection
from models.room import Room

def _map(row) -> Room:
    return Room(*row)

def create(number: str, type: str, area: float, status: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Room (number, type, area, status) VALUES (?, ?, ?, ?)",
        (number, type, area, status)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Room]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT room_id, number, type, area, status FROM Room")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(room_id: int) -> Room | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT room_id, number, type, area, status FROM Room WHERE room_id = ?", (room_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(room_id: int, number: str, type: str, area: float, status: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Room SET number = ?, type = ?, area = ?, status = ? WHERE room_id = ?",
        (number, type, area, status, room_id)
    )
    conn.commit()
    conn.close()

def delete(room_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Room WHERE room_id = ?", (room_id,))
    conn.commit()
    conn.close()