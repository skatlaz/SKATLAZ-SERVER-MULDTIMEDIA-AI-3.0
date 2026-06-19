import sqlite3
from pathlib import Path
from datetime import datetime

class MemoryStore:
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                role TEXT,
                content TEXT,
                created_at TEXT
            )
            """)
            conn.commit()

    def add(self, user_id: str, role: str, content: str):
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO chat_history(user_id, role, content, created_at) VALUES(?,?,?,?)",
                (user_id, role, content, datetime.utcnow().isoformat())
            )
            conn.commit()

    def history(self, user_id: str = "default", limit: int = 20):
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT role, content, created_at FROM chat_history WHERE user_id=? ORDER BY id DESC LIMIT ?",
                (user_id, limit)
            ).fetchall()
        return [{"role": r, "content": c, "created_at": t} for r, c, t in reversed(rows)]
