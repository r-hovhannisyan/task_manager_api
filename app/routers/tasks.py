from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.enums.tasks_enums import Status, TaskSortField, TaskSortOrder
from app.schemas.task_schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_services import (
    create_task,
    delete_task_by_id,
    get_all_tasks,
    get_task_by_id,
    update_task_by_id,
)

router = APIRouter(prefix="/tasks", tags=["Tasks"])

DbSession = Annotated[Session, Depends(get_db)]


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_route(task_data: TaskCreate, db: DbSession):
    try:
        task = create_task(db, task_data)
        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found"
            )
        return task
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task data violates a database constraint",
        )


@router.get("/", response_model=list[TaskResponse])
def get_all_tasks_route(
    db: DbSession,
    status: Status | None = None,
    priority: int | None = None,
    owner_id: int | None = None,
    sort_by: TaskSortField | None = None,
    order: TaskSortOrder = TaskSortOrder.asc,
    page: Annotated[
        int, Query(ge=1, description="Page number. Must be greater than or equal to 1.")
    ] = 1,
    size: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Number of tasks per page. Must be between 1 and 100.",
        ),
    ] = 10,
    search: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=100,
            description="Search tasks by title or description.",
        ),
    ] = None,
):
    return get_all_tasks(
        db=db,
        status=status,
        priority=priority,
        owner_id=owner_id,
        sort_by=sort_by,
        order=order,
        page=page,
        size=size,
        search=search,
    )


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task_by_id_route(task_id: int, db: DbSession):
    task = get_task_by_id(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    return task


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task_by_id_route(task_id: int, task_data: TaskUpdate, db: DbSession):
    task_item = get_task_by_id(db, task_id)

    if task_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
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
            detail="Task data violates a database constraint",
        )


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_by_id_route(task_id: int, db: DbSession):
    task_item = get_task_by_id(db, task_id)

    if task_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    delete_task_by_id(db, task_item)
    return None
