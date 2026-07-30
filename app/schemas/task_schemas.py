from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=150
    )
    description: str | None = Field(
        default=None,
        max_length=1000
    )
    priority: int = Field(
        ge=1,
        le=5
    )
    due_date: datetime | None = None
    owner_id: int


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=150
    )
    description: str | None = Field(
        default=None,
        max_length=1000
    )
    status: Status | None = None
    priority: int | None = Field(
        default=None,
        ge=1,
        le=5
    )
    due_date: datetime | None = None


class TaskResponse(TaskCreate):
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)