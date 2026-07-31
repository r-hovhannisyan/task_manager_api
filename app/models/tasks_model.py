from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.enums.tasks_enums import Status
from app.utils.helpers import utc_now

if TYPE_CHECKING:
    from app.models.users_model import User


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(150))

    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    status: Mapped[Status] = mapped_column(String(20), default="pending", index=True)

    priority: Mapped[int]

    due_date: Mapped[datetime | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        default=utc_now, server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        default=utc_now, server_default=func.now(), onupdate=utc_now
    )

    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )

    owner: Mapped["User"] = relationship(back_populates="tasks")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'in_progress', 'completed')",
            name="check_task_status",
        ),
        CheckConstraint(
            "priority BETWEEN 1 AND 5",
            name="check_task_priority",
        ),
    )
