from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.schemas.task_schemas import TaskResponse


class UserCreate(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50
    )
    email: EmailStr
    first_name: str = Field(
        min_length=1,
        max_length=100
    )
    last_name: str = Field(
        min_length=1,
        max_length=100
    )

class UserResponse(UserCreate):
    id: int
    created_at: datetime
    tasks: list[TaskResponse]
    model_config = ConfigDict(from_attributes=True)