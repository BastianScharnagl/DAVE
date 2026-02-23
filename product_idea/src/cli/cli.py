"""
Command Line Interface for Smart Task Optimizer
"""

import argparse
import datetime
from product_idea.src.core.task import Task
from product_idea.src.core.priority_engine import PriorityEngine
from product_idea.src.scheduler.scheduler import Scheduler

class TaskCLI:
    """Command-line interface for task management"""
    
    def __init__(self):
        self.tasks = []
        self.priority_engine = PriorityEngine()
        self.scheduler = Scheduler()
        self.scheduler.priority_engine = self.priority_engine
    
    def add_task(self, title, description="", priority=1, effort=1, deadline=None, tags=None):
        """Add a new task"""
        task = Task(title, description, priority, effort, deadline, tags or [])
        self.tasks.append(task)
        print(f"✓ Added task: {task}")
        
    def list_tasks(self, show_completed=False):
        """List all tasks"""
        tasks = self.tasks if show_completed else [t for t in self.tasks if not t.completed]
        
        if not tasks:
            print("No tasks found.")
            return
        
        # Rank tasks by priority
        ranked = self.priority_engine.rank_tasks(tasks)
        
        print(f"\n{'ID':<4} {'Priority':<10} {'Title':<30} {'Effort':<8} {'Deadline':<15}")
        print("─" * 70)
        
        for i, (task, score) in enumerate(ranked, 1):
            deadline_str = task.deadline.strftime("%Y-%m-%d") if task.deadline else "None"
            print(f"{i:<4} {score:<10.1f} {task.title:<30} {task.effort:<8} {deadline_str:<15}")

    def schedule_day(self, date=None):
        """Generate schedule for a day"""
        if date is None:
            date = datetime.datetime.now().date()
            
        # Get active tasks
        active_tasks = [t for t in self.tasks if not t.completed]
        
        if not active_tasks:
            print("No active tasks to schedule.")
            return

        # Set start time to 9am
        start_time = datetime.datetime.combine(date, datetime.time(9, 0))
        
        # Generate 8-hour schedule
        schedule = self.scheduler.generate_schedule(active_tasks, start_time, 8 * 60)
        
        if not schedule:
            print("Could not generate schedule.")
            return

        print(f"\nSchedule for {date}:")
        print("─" * 50)
        
        for item in schedule:
            start = item['start_time'].strftime("%H:%M")
            end = item['end_time'].strftime("%H:%M")
            task = item['task']
            print(f"{start} - {end} | [{task.priority}] {task.title} ({task.effort} effort)")

    def run(self):
        """Run the CLI interface"""
        parser = argparse.ArgumentParser(description='Smart Task Optimizer')
        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Add command
        parser_add = subparsers.add_parser('add', help='Add a new task')
        parser_add.add_argument('title', help='Task title')
        parser_add.add_argument('--description', '-d', help='Task description')
        parser_add.add_argument('--priority', '-p', type=int, choices=range(1,6), 
                               default=1, help='Priority level (1-5)')
        parser_add.add_argument('--effort', '-e', type=int, choices=range(1,6), 
                               default=1, help='Effort level (1-5)')
        parser_add.add_argument('--deadline', '-dl', help='Deadline (YYYY-MM-DD)')
        parser_add.add_argument('--tags', '-t', nargs='+', help='Tags for the task')

        # List command
        parser_list = subparsers.add_parser('list', help='List tasks')
        parser_list.add_argument('--all', '-a', action='store_true', 
                                help='Show completed tasks too')

        # Schedule command
        parser_schedule = subparsers.add_parser('schedule', help='Generate schedule')
        parser_schedule.add_argument('--date', '-d', help='Date for schedule (YYYY-MM-DD)')

        args = parser.parse_args()

        if args.command == 'add':
            deadline = None
            if args.deadline:
                deadline = datetime.datetime.strptime(args.deadline, "%Y-%m-%d")
            
            self.add_task(
                args.title,
                args.description or "",
                args.priority,
                args.effort,
                deadline,
                args.tags
            )
        
        elif args.command == 'list':
            self.list_tasks(args.all)
        
        elif args.command == 'schedule':
            date = None
            if args.date:
                date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
            self.schedule_day(date)
        
        else:
            parser.print_help()