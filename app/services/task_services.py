from sqlalchemy import asc, desc, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.enums.tasks_enums import Status, TaskSortField, TaskSortOrder
from app.models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.services.user_services import get_user_by_id

SORT_COLUMNS = {
    TaskSortField.priority: Task.priority,
    TaskSortField.created_at: Task.created_at,
    TaskSortField.due_date: Task.due_date,
    TaskSortField.status: Task.status,
}


def create_task(db: Session, task_data: TaskCreate) -> Task | None:
    if get_user_by_id(db, task_data.owner_id) is None:
        return None

    new_task = Task(**task_data.model_dump())

    db.add(new_task)

    try:
        db.commit()
        db.refresh(new_task)
        return new_task
    except IntegrityError:
        db.rollback()
        raise


def get_all_tasks(
    db: Session,
    status: Status | None = None,
    priority: int | None = None,
    owner_id: int | None = None,
    sort_by: TaskSortField | None = None,
    order: TaskSortOrder = TaskSortOrder.asc,
    page: int = 1,
    size: int = 10,
    search: str | None = None,
) -> list[Task]:
    tasks_offset = (page - 1) * size
    stmt = select(Task)

    if status is not None:
        stmt = stmt.where(Task.status == status.value)

    if priority is not None:
        stmt = stmt.where(Task.priority == priority)

    if owner_id is not None:
        stmt = stmt.where(Task.owner_id == owner_id)

    if search is not None:
        search = search.strip()

        if search:
            pattern = f"%{search}%"

            stmt = stmt.where(
                or_(Task.title.ilike(pattern), Task.description.ilike(pattern))
            )

    if sort_by is not None:
        column = SORT_COLUMNS[sort_by]

        if order == TaskSortOrder.desc:
            stmt = stmt.order_by(desc(column))
        else:
            stmt = stmt.order_by(asc(column))
    else:
        stmt = stmt.order_by(asc(Task.id))

    stmt = stmt.offset(tasks_offset).limit(size)

    return list(db.scalars(stmt))


def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def update_task_by_id(
    db: Session, task_item: Task, task_data: TaskUpdate
) -> Task | None:
    update_data = task_data.model_dump(exclude_unset=True)

    if "owner_id" in update_data:
        new_owner_id = update_data["owner_id"]

        if new_owner_id is None:
            return None

        if get_user_by_id(db, new_owner_id) is None:
            return None

    for field, value in update_data.items():
        setattr(task_item, field, value)

    try:
        db.commit()
        db.refresh(task_item)
        return task_item
    except IntegrityError:
        db.rollback()
        raise


def delete_task_by_id(db: Session, task_item: Task) -> None:
    db.delete(task_item)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
