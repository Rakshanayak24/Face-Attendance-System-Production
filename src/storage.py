import sqlite3
import os
import time

class AttendanceDB:
    def __init__(self, db_file="data/attendance.db"):
        self.db_file = db_file
        os.makedirs(os.path.dirname(db_file), exist_ok=True)
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            status TEXT,
            timestamp TEXT
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def mark(self, name, status="IN"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            "INSERT INTO attendance (name, status, timestamp) VALUES (?, ?, ?)",
            (name, status, timestamp)
        )
        self.conn.commit()
        print(f"[DB] {name} marked {status} at {timestamp}")

    def get_last_status(self, name):
        cursor = self.conn.execute(
            "SELECT status FROM attendance WHERE name=? ORDER BY id DESC LIMIT 1", (name,)
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            return "OUT"  # Default so first time punches IN
