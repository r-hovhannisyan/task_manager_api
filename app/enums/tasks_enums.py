from enum import Enum


class TaskSortField(str, Enum):
    priority = "priority"
    created_at = "created_at"
    due_date = "due_date"
    status = "status"


class TaskSortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


class Status(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
