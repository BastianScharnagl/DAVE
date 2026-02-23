# Smart Task Optimizer - User Guide

Welcome to the Smart Task Optimizer! This guide will help you get started with managing your tasks more efficiently.

## Installation

```bash
pip install smart-task-optimizer
```

## Quick Start

### 1. Create Your First Task

```python
from product_idea.src.core.task import Task
from datetime import datetime, timedelta

# Create a task
my_task = Task(
    title="Complete project proposal",
    description="Write and review the Q3 project proposal",
    priority=3,
    estimated_time=120,
    deadline=datetime.now() + timedelta(days=2)
)
```

### 2. Prioritize Your Tasks

```python
from product_idea.src.core.priority_engine import PriorityEngine

# Create priority engine
engine = PriorityEngine()

# Create multiple tasks
tasks = [
    Task("Urgent meeting", "Prepare for client call", 3, 60, datetime.now() + timedelta(hours=1)),
    Task("Report writing", "Complete monthly report", 2, 180, datetime.now() + timedelta(days=3)),
    Task("Emails", "Respond to pending emails", 1, 45, datetime.now() + timedelta(days=1))
]

# Sort tasks by priority
prioritized_tasks = engine.sort_by_priority(tasks)
```

### 3. Generate Your Schedule

```python
from product_idea.src.scheduler.scheduler import Scheduler

# Create scheduler
scheduler = Scheduler()

# Generate schedule for 8 hours
from datetime import datetime
start_time = datetime.now()
duration_minutes = 480  # 8 hours

schedule = scheduler.generate_schedule(prioritized_tasks, start, duration_minutes)
```

## Key Features

### Intelligent Prioritization
The Priority Engine automatically scores your tasks based on:
- Urgency (how soon the deadline is)
- Importance (your assigned priority level)
- Estimated time to complete
- Deadline proximity

### Smart Scheduling
The Scheduler allocates time blocks for your tasks, ensuring you focus on the most important items first while respecting your available time.

### Learning System
The Task Optimizer learns from your behavior over time, improving its suggestions based on which tasks you actually complete and when.

## Best Practices

1. **Be Realistic with Time Estimates**: Accurate time estimates help the scheduler work effectively
2. **Update Task Status**: Mark tasks as complete to help the learning system improve
3. **Review Regularly**: Check your prioritized task list daily to stay on track
4. **Adjust Priorities**: Update task priorities as circumstances change

## Support
For questions or issues, please contact support@smarttaskoptimizer.com