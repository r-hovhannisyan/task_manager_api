from typing import TYPE_CHECKING

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.utils.helpers import utc_now
from app.database import Base

if TYPE_CHECKING:
    from app.models.tasks_model import Task


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)

    first_name: Mapped[str] = mapped_column(String(100))

    last_name: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        default=utc_now, server_default=func.now()
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )
