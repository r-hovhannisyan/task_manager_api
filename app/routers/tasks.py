from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter, Depends, status, HTTPException

from app.database import get_db
from app.schemas.task_schemas import TaskResponse, TaskCreate, TaskUpdate
from app.services.task_services import delete_task_by_id, get_task_by_id, get_all_tasks, update_task_by_id, create_task

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

DbSession = Annotated[Session, Depends(get_db)]

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_route(task_data: TaskCreate ,db:DbSession):
    try:
        task = create_task(db, task_data)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Owner not found"
            )
        return task
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task data violates a database constraint"
        )

@router.get("/", response_model=list[TaskResponse])
def get_all_tasks_route(db: DbSession):
    return get_all_tasks(db)

@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id_route(task_id: int, db: DbSession):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_by_id_route(task_id: int, task_data: TaskUpdate, db: DbSession):
    task_item = get_task_by_id(db, task_id)

    if task_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    try:
        updated_task = update_task_by_id(db, task_item, task_data)

        if updated_task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New owner not found",
            )

        return updated_task
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task data violates a database constraint"
        )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id_route(task_id: int, db: DbSession):
    task_item = get_task_by_id(db, task_id)

    if task_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    delete_task_by_id(db, task_item)
    return None