from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.users_model import User
from app.schemas.user_schemas import UserCreate


def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(**user.model_dump())

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise


def get_all_users(db: Session) -> list[User]:
    stmt = select(User)
    return list(db.scalars(stmt))


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.get(User, user_id)


def delete_user_by_id(db: Session, user_item: User):
    db.delete(user_item)
    db.commit()
