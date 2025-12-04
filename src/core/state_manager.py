import json
import os
from typing import Dict, List, Optional
from .task_model import Task, TaskStatus

class StateManager:
    def __init__(self, data_file: str = "data/tasks.json"):
        self.data_file = data_file
        self.tasks: Dict[str, Task] = {}
        self.root_task_ids: List[str] = [] # Top level tasks
        self.load_state()

    def load_state(self):
        if not os.path.exists(self.data_file):
            self.tasks = {}
            self.root_task_ids = []
            return

        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.tasks = {t_data['id']: Task.from_dict(t_data) for t_data in data.get('tasks', [])}
                self.root_task_ids = data.get('root_task_ids', [])
        except (json.JSONDecodeError, IOError):
            self.tasks = {}
            self.root_task_ids = []

    def save_state(self):
        data = {
            'tasks': [t.to_dict() for t in self.tasks.values()],
            'root_task_ids': self.root_task_ids
        }
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_task(self, title: str, description: str = "", parent_id: Optional[str] = None, is_reward: bool = False) -> Task:
        new_task = Task(title=title, description=description, parent_id=parent_id, is_reward=is_reward)
        self.tasks[new_task.id] = new_task
        
        if parent_id:
            parent = self.tasks.get(parent_id)
            if parent:
                parent.children_ids.append(new_task.id)
        else:
            self.root_task_ids.append(new_task.id)
            
        self.save_state()
        return new_task

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def update_task_status(self, task_id: str, status: TaskStatus):
        task = self.tasks.get(task_id)
        if task:
            task.status = status
            self.save_state()

    def get_next_actionable_task(self) -> Optional[Task]:
        """
        Finds the first actionable task (DFS).
        A task is actionable if:
        1. It is PENDING or ACTIVE.
        2. It has no children (leaf node) OR all children are COMPLETED/SKIPPED.
        """
        # Simple DFS to find the first leaf node that is pending/active
        # We prioritize existing active tasks
        
        # First check if there is an active task
        for task in self.tasks.values():
            if task.status == TaskStatus.ACTIVE:
                 # If it has open children, it's not the leaf action, its children are.
                 # But if we are strictly following "one thing", maybe we should check children.
                 # Let's use a recursive helper.
                 pass

        # Let's iterate through roots and find the first available
        for root_id in self.root_task_ids:
            task = self._find_next_in_subtree(root_id)
            if task:
                return task
        return None

    def _find_next_in_subtree(self, task_id: str) -> Optional[Task]:
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        if task.status in [TaskStatus.COMPLETED, TaskStatus.SKIPPED]:
            return None

        # If it has children, look into them first
        if task.children_ids:
            # Check if all children are done?
            # We want to do the first pending child.
            for child_id in task.children_ids:
                found = self._find_next_in_subtree(child_id)
                if found:
                    return found
            
            # If we are here, all children are done (or skipped).
            # So this task itself is now "done" effectively, or ready to be marked done.
            # But wait, if it's a container task, maybe it doesn't need manual completion?
            # For now, let's say if all children are done, the user still needs to explicitly 
            # mark this parent task as done (maybe it was "Clean Room", children were "Floor", "Desk". 
            # After Floor and Desk, user says "Clean Room" is done).
            return task
        else:
            # It's a leaf node and it is PENDING/ACTIVE (checked above)
            return task

    def delete_task(self, task_id: str):
        # This is complex because of children. For now, let's just remove from parent and dict.
        task = self.tasks.get(task_id)
        if not task:
            return
            
        if task.parent_id:
            parent = self.tasks.get(task.parent_id)
            if parent and task_id in parent.children_ids:
                parent.children_ids.remove(task_id)
        else:
            if task_id in self.root_task_ids:
                self.root_task_ids.remove(task_id)
        
        # Recursive delete children? Or orphan them? Let's recursive delete.
        self._delete_recursive(task_id)
        self.save_state()

    def _delete_recursive(self, task_id: str):
        task = self.tasks.get(task_id)
        if not task:
            return
        for child_id in list(task.children_ids):
            self._delete_recursive(child_id)
        if task_id in self.tasks:
            del self.tasks[task_id]
