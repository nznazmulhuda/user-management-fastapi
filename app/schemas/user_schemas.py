from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str
    email: EmailStr
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com"
            }
        }


class UserUpdate(BaseModel):
    """Schema for updating a user."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "johndoe_updated",
                "email": "newemail@example.com"
            }
        }


class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    username: str
    email: str
    created_at: str
    
    class Config:
        from_attributes = True
