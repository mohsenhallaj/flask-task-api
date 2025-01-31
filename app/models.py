from enum import Enum

class StatusEnum(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in progress"
    COMPLETED = "completed"

def to_dict(task):
    return {
        "id": str(task.get("_id")),
        "title": task.get("title"),
        "description": task.get("description"),
        "status": task.get("status"),
        "created_at": task.get("created_at"),
        "updated_at": task.get("updated_at"),
    }
