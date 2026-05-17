import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from .config import settings


DB_PATH = Path(settings.DATABASE_PATH)
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                company_name TEXT NOT NULL,
                company_website TEXT NOT NULL,
                status TEXT NOT NULL,
                report_path TEXT,
                error TEXT,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
            """
        )
        conn.commit()


def insert_lead(full_name: str, email: str, company_name: str, company_website: str) -> int:
    now = datetime.utcnow()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO leads (full_name, email, company_name, company_website, status, created_at, updated_at)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (full_name, email, company_name, company_website, "processing", now, now),
        )
        conn.commit()
        return cursor.lastrowid


def update_lead_status(lead_id: int, status: str, report_path: str | None = None, error: str | None = None) -> None:
    now = datetime.utcnow()
    with get_connection() as conn:
        conn.execute(
            "UPDATE leads SET status = ?, report_path = ?, error = ?, updated_at = ? WHERE id = ?",
            (status, report_path, error, now, lead_id),
        )
        conn.commit()


def fetch_lead_by_id(lead_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        cursor = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
