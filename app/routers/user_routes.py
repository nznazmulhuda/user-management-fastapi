from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas.user_schemas import UserCreate, UserUpdate, UserResponse
from app.crud import user_crud

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user.
    
    - **username**: Unique username for the user
    - **email**: Unique email address for the user
    """
    try:
        created_user = user_crud.create_user(user)
        return created_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=List[UserResponse])
async def get_all_users():
    """
    Retrieve all users from the database.
    
    Returns a list of all users ordered by creation date (newest first).
    """
    users = user_crud.get_all_users()
    return users


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Retrieve a specific user by ID.
    
    - **user_id**: The ID of the user to retrieve
    """
    user = user_crud.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Update a user's information.
    
    - **user_id**: The ID of the user to update
    - **username**: New username (optional)
    - **email**: New email address (optional)
    """
    try:
        updated_user = user_crud.update_user(user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    Delete a user from the database.
    
    - **user_id**: The ID of the user to delete
    """
    deleted = user_crud.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    return None
