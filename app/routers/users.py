from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.schemas.user_schemas import UserResponse, UserCreate
from app.services.user_services import create_user, get_user_by_id, get_all_users, delete_user_by_id
router = APIRouter(prefix="/users", tags=["Users"])
DbSession = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user_route(user_data: UserCreate, db: DbSession):
    try:
        return create_user(db, user_data)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists"
        )

@router.get("/", response_model=list[UserResponse])
def get_all_users_route(db: DbSession):
    return get_all_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id_route(user_id: int, db: DbSession):
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_id_route(user_id: int, db: DbSession):
    user_item = get_user_by_id(db, user_id)

    if user_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    delete_user_by_id(db, user_item)
    return None

