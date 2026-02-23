"""
Task module for Smart Task Optimizer
Handles task creation, storage, and basic operations
"""

class Task:
    """Represents a single task with properties for prioritization"""
    
    def __init__(self, title, description="", priority=1, effort=1, deadline=None, tags=None):
        self.title = title
        self.description = description
        self.priority = priority  # 1-5, 5 being highest
        self.effort = effort      # 1-5, 5 being most effort
        self.deadline = deadline  # datetime object
        self.tags = tags or []
        self.completed = False
        self.created_at = None
        self.updated_at = None
        
    def __str__(self):
        return f"[{self.priority}] {self.title} (Effort: {self.effort})"
    
    def __repr__(self):
        return f"Task('{self.title}', priority={self.priority}, effort={self.effort})"


class TaskManager:
    """Manages a collection of tasks"""
    
    def __init__(self):
        self.tasks = []
        
    def add_task(self, task):
        """Add a task to the collection"""
        self.tasks.append(task)
        
    def remove_task(self, task):
        """Remove a task from the collection"""
        self.tasks.remove(task)
        
    def get_active_tasks(self):
        """Return all incomplete tasks"""
        return [task for task in self.tasks if not task.completed]
        
    def get_completed_tasks(self):
        """Return all completed tasks"""
        return [task for task in self.tasks if task.completed]
        
    def find_tasks_by_tag(self, tag):
        """Find all tasks with a specific tag"""
        return [task for task in self.tasks if tag in task.tags]