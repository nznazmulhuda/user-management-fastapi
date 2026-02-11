from typing import List, Optional
from app.database import get_db
from app.schemas.user_schemas import UserCreate, UserUpdate
import sqlite3


def create_user(user: UserCreate) -> dict:
    """Create a new user in the database."""
    with get_db() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, email) VALUES (?, ?)",
                (user.username, user.email)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            # Fetch the created user
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            return dict(row)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"User with this username or email already exists: {str(e)}")


def get_all_users() -> List[dict]:
    """Retrieve all users from the database."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_user_by_id(user_id: int) -> Optional[dict]:
    """Retrieve a user by ID."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def update_user(user_id: int, user_update: UserUpdate) -> Optional[dict]:
    """Update a user's information."""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Check if user exists
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            return None
        
        # Build update query dynamically based on provided fields
        update_fields = []
        values = []
        
        if user_update.username is not None:
            update_fields.append("username = ?")
            values.append(user_update.username)
        
        if user_update.email is not None:
            update_fields.append("email = ?")
            values.append(user_update.email)
        
        if not update_fields:
            # No fields to update, return current user
            return get_user_by_id(user_id)
        
        values.append(user_id)
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return get_user_by_id(user_id)
        except sqlite3.IntegrityError as e:
            raise ValueError(f"Update failed - username or email already exists: {str(e)}")


def delete_user(user_id: int) -> bool:
    """Delete a user from the database."""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
