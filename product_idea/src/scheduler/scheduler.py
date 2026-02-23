"""
Scheduler module for Smart Task Optimizer
Handles task scheduling and time allocation
"""

class Scheduler:
    """Generates optimal schedules based on task priorities and time availability"""
    
    def __init__(self):
        self.priority_engine = None
    
    def generate_schedule(self, tasks, start_time, duration_minutes):
        """Generate an optimized schedule for a list of tasks
        
        Args:
            tasks: List of Task objects to schedule
            start_time: Starting datetime for the schedule
            duration_minutes: Total time available in minutes
        
        Returns:
            List of scheduled tasks with start and end times
        """
        if not tasks or duration_minutes <= 0:
            return []
            
        # Sort tasks by priority (assuming priority engine is set)
        if self.priority_engine:
            sorted_tasks = self.priority_engine.sort_by_priority(tasks)
        else:
            # Default sort by priority level if no engine available
            sorted_tasks = sorted(tasks, key=lambda x: x.priority, reverse=True)
        
        schedule = []
        current_time = start_time
        time_remaining = duration_minutes
        
        for task in sorted_tasks:
            # Skip tasks that can't fit in remaining time
            if task.estimated_time > time_remaining:
                continue
                
            # Add task to schedule
            end_time = current_time + timedelta(minutes=task.estimated_time)
            schedule.append({
                'task': task,
                'start_time': current_time,
                'end_time': end_time
            })
            
            # Update time
            current_time = end_time
            time_remaining -= task.estimated_time
            
            if time_remaining <= 0:
                break

        return schedule