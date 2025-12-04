import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    SKIPPED = "skipped"

@dataclass
class Task:
    title: str
    description: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus = TaskStatus.PENDING
    children_ids: List[str] = field(default_factory=list)
    parent_id: Optional[str] = None
    is_reward: bool = False
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "children_ids": self.children_ids,
            "parent_id": self.parent_id,
            "is_reward": self.is_reward
        }

    @classmethod
    def from_dict(cls, data):
        task = cls(
            id=data["id"],
            title=data["title"],
            description=data.get("description", ""),
            status=TaskStatus(data["status"]),
            children_ids=data.get("children_ids", []),
            parent_id=data.get("parent_id"),
            is_reward=data.get("is_reward", False)
        )
        return task
