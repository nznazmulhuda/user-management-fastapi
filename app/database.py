import sqlite3
import os
from contextlib import contextmanager
from pathlib import Path
from platformdirs import user_data_dir

# 1. Define the App Name and Author
APP_NAME = "user-management"
APP_AUTHOR = "nazmulhuda"

# 2. Get the OS-specific data directory
# Windows: C:\Users\User\AppData\Local\YourCompany\TengenApp
# macOS: ~/Library/Application Support/TengenApp
# Linux: ~/.local/share/TengenApp
APP_DATA_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR))
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = APP_DATA_DIR / "users.db"

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()


@contextmanager
def get_db():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This allows us to access columns by name
    try:
        yield conn
    finally:
        conn.close()
