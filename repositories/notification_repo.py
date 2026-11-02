from database.db import get_connection
from models.notification import Notification

def _map(row) -> Notification:
    return Notification(*row)

def create(room_id: int, employee_id: int, description: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO Notification (room_id, employee_id, description) VALUES (?, ?, ?)",
        (room_id, employee_id, description)
    )
    conn.commit()
    conn.close()

def get_all() -> list[Notification]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT notification_id, room_id, employee_id, description FROM Notification")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]

def get_by_id(notification_id: int) -> Notification | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT notification_id, room_id, employee_id, description FROM Notification WHERE notification_id = ?", (notification_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None

def update(notification_id: int, room_id: int, employee_id: int, description: str) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE Notification SET room_id = ?, employee_id = ?, description = ? WHERE notification_id = ?",
        (room_id, employee_id, description, notification_id)
    )
    conn.commit()
    conn.close()

def delete(notification_id: int) -> None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Notification WHERE notification_id = ?", (notification_id,))
    conn.commit()
    conn.close()