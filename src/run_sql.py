import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


DB_PATH = os.path.join(BASE_DIR, "..", "rental.db")


SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")


with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    sql_script = f.read()

cursor.executescript(sql_script)

conn.commit()
conn.close()
print("База данных создана, данные добавлены.")