import re
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Application constants
APP_NAME = "Task Manager"
APP_VERSION = "1.0"
DATA_FILE = "tasks.json"
BACKUP_FILE = "tasks_backup.json"

# Priority levels
PRIORITY_LEVELS = ["low", "medium", "high"]
PRIORITY_COLORS = {
    "low": "green",
    "medium": "yellow", 
    "high": "red"
}

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_priority(priority: str) -> bool:
    """Validate priority level"""
    return priority.lower() in PRIORITY_LEVELS

def format_date(date_string: str) -> str:
    """Format date string for display"""
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except ValueError:
        return date_string

def calculate_days_since(date_string: str) -> int:
    """Calculate days since a given date"""
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return (datetime.now() - dt).days
    except ValueError:
        return 0

def clean_string(text: str) -> str:
    """Clean and normalize string input"""
    if not text:
        return ""
    return ' '.join(text.strip().split())

def truncate_text(text: str, max_length: int = 50) -> str:
    """Truncate text to specified length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def get_priority_symbol(priority: str) -> str:
    """Get symbol for priority level"""
    symbols = {
        "low": "↓",
        "medium": "→", 
        "high": "↑"
    }
    return symbols.get(priority.lower(), "→")

def sort_tasks_by_priority(tasks: List[Any]) -> List[Any]:
    """Sort tasks by priority (high to low)"""
    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(tasks, key=lambda t: priority_order.get(t.priority, 1))

def sort_tasks_by_date(tasks: List[Any], reverse: bool = False) -> List[Any]:
    """Sort tasks by creation date"""
    return sorted(tasks, key=lambda t: t.created_at, reverse=reverse)

def filter_tasks_by_keyword(tasks: List[Any], keyword: str) -> List[Any]:
    """Filter tasks by keyword in title or description"""
    if not keyword:
        return tasks
    
    keyword_lower = keyword.lower()
    return [
        task for task in tasks 
        if keyword_lower in task.title.lower() or 
           keyword_lower in task.description.lower()
    ]

def get_completion_percentage(completed: int, total: int) -> float:
    """Calculate completion percentage"""
    if total == 0:
        return 0.0
    return (completed / total) * 100

def create_progress_bar(percentage: float, width: int = 20) -> str:
    """Create a text-based progress bar"""
    filled = int(width * percentage / 100)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {percentage:.1f}%"

def get_app_info() -> Dict[str, str]:
    """Get application information"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "author": "Task Manager Team",
        "description": "A simple command-line task management application"
    }

def generate_backup_filename() -> str:
    """Generate backup filename with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"tasks_backup_{timestamp}.json"

def is_valid_date_format(date_string: str) -> bool:
    """Check if date string is in valid format"""
    try:
        datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def get_relative_time(date_string: str) -> str:
    """Get relative time description"""
    try:
        dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        diff = datetime.now() - dt
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    except ValueError:
        return "Unknown"

class TaskCounter:
    """Utility class for counting tasks"""
    
    def __init__(self, tasks: List[Any]):
        self.tasks = tasks
    
    def total(self) -> int:
        """Get total task count"""
        return len(self.tasks)
    
    def completed(self) -> int:
        """Get completed task count"""
        return len([t for t in self.tasks if t.completed])
    
    def pending(self) -> int:
        """Get pending task count"""
        return len([t for t in self.tasks if not t.completed])
    
    def by_priority(self, priority: str) -> int:
        """Get task count by priority"""
        return len([t for t in self.tasks if t.priority == priority.lower()])
    
    def created_today(self) -> int:
        """Get tasks created today"""
        today = datetime.now().date()
        count = 0
        for task in self.tasks:
            try:
                task_date = datetime.strptime(task.created_at, "%Y-%m-%d %H:%M:%S").date()
                if task_date == today:
                    count += 1
            except ValueError:
                continue
        return count
    
    def completed_today(self) -> int:
        """Get tasks completed today"""
        today = datetime.now().date()
        count = 0
        for task in self.tasks:
            if task.completed and task.completed_at:
                try:
                    completed_date = datetime.strptime(task.completed_at, "%Y-%m-%d %H:%M:%S").date()
                    if completed_date == today:
                        count += 1
                except ValueError:
                    continue
        return count