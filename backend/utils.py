import os
import sqlite3
import json
from typing import List, Optional
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str

class SessionManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to sessions.db in the same directory as this file (backend/)
            base_dir = os.path.dirname(os.path.abspath(__file__))
            self.db_path = os.path.join(base_dir, 'sessions.db')
        else:
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
            conn.execute("""
                CREATE TABLE IF NOT EXISTS allowed_users (
                    username TEXT PRIMARY KEY,
                    added_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_session_id ON chat_sessions(session_id)")

    def is_user_allowed(self, username: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT 1 FROM allowed_users WHERE username = ?", (username.lower(),))
            return cursor.fetchone() is not None

    def add_user(self, username: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("INSERT OR IGNORE INTO allowed_users (username) VALUES (?)", (username.lower(),))

    def remove_user(self, username: str):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM allowed_users WHERE username = ?", (username.lower(),))

    def get_all_users(self) -> List[str]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT username FROM allowed_users")
            return [row[0] for row in cursor.fetchall()]

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
