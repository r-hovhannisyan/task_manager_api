from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.services.user_services import get_user_by_id


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

def get_all_tasks(db: Session) -> list[Task]:
    stmt = select(Task)
    return list(db.scalars(stmt))

def get_task_by_id(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)

def update_task_by_id(db: Session, task_item: Task, task_data: TaskUpdate) -> Task | None:
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