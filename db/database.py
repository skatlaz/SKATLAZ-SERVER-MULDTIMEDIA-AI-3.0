import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "bd.sqlite3"

class Database:
    def __init__(self):
        # Django dev server may handle requests in different threads.
        # Do not share one sqlite connection/cursor between requests.
        self.conn = sqlite3.connect(str(DB_NAME), check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            source TEXT,
            content TEXT,
            score REAL DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT,
            answer TEXT,
            source TEXT,
            embedding TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def save_question(self, prompt):
        self.cursor.execute("INSERT INTO questions (prompt) VALUES (?)", (prompt,))
        self.conn.commit()
        return self.cursor.lastrowid

    def save_response(self, question_id, source, content, score=0):
        self.cursor.execute(
            "INSERT INTO responses (question_id, source, content, score) VALUES (?, ?, ?, ?)",
            (question_id, source, content, score)
        )
        self.conn.commit()

    def train(self, question, answer, source="manual_train"):
        self.cursor.execute(
            "INSERT INTO training_data (question, answer, source) VALUES (?, ?, ?)",
            (question, answer, source)
        )
        self.conn.commit()

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception:
            pass
