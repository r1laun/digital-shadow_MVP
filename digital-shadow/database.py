import sqlite3
import json
from datetime import datetime

DB_PATH = "digital_shadow.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT,
            category TEXT,
            risk_level TEXT,
            risk_score INTEGER,
            summary TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_result(query: str, result: dict):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO searches (query, category, risk_level, risk_score, summary, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        query,
        result.get("category", ""),
        result.get("risk_level", ""),
        result.get("risk_score", 0),
        result.get("summary", ""),
        datetime.now().strftime("%Y-%m-%d %H:%M"),
    ))
    conn.commit()
    conn.close()

def get_history(limit: int = 10) -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT * FROM searches ORDER BY id DESC LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]
