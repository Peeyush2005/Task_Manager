import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Task:
    """Represents a single task"""
    
    def __init__(self, title: str, description: str = "", priority: str = "medium"):
        self.id = self._generate_id()
        self.title = title
        self.description = description
        self.priority = priority.lower()
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None
        
        # Validate priority
        if self.priority not in ["low", "medium", "high"]:
            self.priority = "medium"
    
    def _generate_id(self) -> str:
        """Generate a unique task ID"""
        return str(int(datetime.now().timestamp() * 1_000_000))
    
    def mark_complete(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def mark_incomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.completed_at = None
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None, priority: Optional[str] = None):
        """Update task details"""
        if title is not None and title.strip():
            self.title = title.strip()
        if description is not None:
            self.description = description
        if priority:
            priority = priority.lower()
            if priority in ["low", "medium", "high"]:
                self.priority = priority
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "completed": self.completed,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Create task from dictionary"""
        task = cls(data["title"], data.get("description", ""), data.get("priority", "medium"))
        task.id = data["id"]
        task.completed = data.get("completed", False)
        task.created_at = data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        task.completed_at = data.get("completed_at")
        return task
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        priority_symbol = {"low": "↓", "medium": "→", "high": "↑"}.get(self.priority, "→")
        return f"[{status}] {priority_symbol} {self.title}"


class TaskManager:
    """Main task management class"""
    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
    
    def add_task(self, title: str, description: str = "", priority: str = "medium") -> Task:
        """Add a new task"""
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        
        task = Task(title.strip(), description.strip(), priority)
        self.tasks.append(task)
        return task
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.tasks.copy()
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all incomplete tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_completed_tasks(self) -> List[Task]:
        """Get all completed tasks"""
        return [task for task in self.tasks if task.completed]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """Get tasks by priority level"""
        priority = priority.lower()
        return [task for task in self.tasks if task.priority == priority]
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        data = [task.to_dict() for task in self.tasks]
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.filename):
            raise FileNotFoundError(f"File {self.filename} not found")
        
        with open(self.filename, 'r') as f:
            data = json.load(f)
        
        self.tasks = [Task.from_dict(task_data) for task_data in data]
    
    def get_stats(self) -> Dict:
        """Get task statistics"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())
        
        priority_counts = {"low": 0, "medium": 0, "high": 0}
        for task in self.tasks:
            if task.priority in priority_counts:
                priority_counts[task.priority] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "priority_counts": priority_counts
        }
