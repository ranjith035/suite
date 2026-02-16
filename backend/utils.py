import os
import sqlite3
import json
from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class SessionManager:
    def __init__(self, db_path='sessions.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chat_sessions (
                    session_id TEXT,
                    role TEXT,
                    content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON chat_sessions(session_id)")

    def save_message(self, session_id: str, role: str, content: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO chat_sessions (session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content)
            )

    def get_history(self, session_id: str) -> List[Message]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT role, content FROM chat_sessions WHERE session_id = ? ORDER BY timestamp ASC",
                (session_id,)
            )
            rows = cursor.fetchall()
            return [Message(role=row[0], content=row[1]) for row in rows]

    def clear_history(self, session_id: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM chat_sessions WHERE session_id = ?", (session_id,))

class TokenManager:
    """
    Handles fetching and caching the organization's access token.
    """
    def __init__(self, auth_api_url: Optional[str] = None):
        self.auth_api_url = auth_api_url
        self._token = None

    def get_token(self) -> str:
        return os.getenv("GOOGLE_ACCESS_TOKEN", "mock-token")
