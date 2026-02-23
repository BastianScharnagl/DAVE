import unittest
from datetime import datetime, timedelta
from unittest.mock import Mock
from product_idea.src.scheduler.scheduler import Scheduler
from product_idea.src.core.task import Task

class TestScheduler(unittest.TestCase):
    
    def setUp(self):
        self.scheduler = Scheduler()
        self.mock_priority_engine = Mock()
        self.scheduler.priority_engine = self.mock_priority_engine
    
    def test_generate_schedule(self):
        # Create test tasks
        tasks = [
            Task("Task 1", "", 3, 60, datetime.now() + timedelta(hours=2)),
            Task("Task 2", "", 2, 90, datetime.now() + timedelta(hours=3)),
            Task("Task 3", "", 1, 30, datetime.now() + timedelta(hours=4))
        ]
        
        # Mock priority engine behavior
        self.mock_priority_engine.sort_by_priority.return_value = tasks
        
        # Generate schedule for 4 hours starting now
        start_time = datetime.now()
        duration = 4 * 60  # 4 hours in minutes
        
        schedule = self.scheduler.generate_schedule(tasks, start_time, duration)
        
        # Check that schedule is generated
        self.assertIsInstance(schedule, list)
        self.assertGreater(len(schedule), 0)
        
        # Check that first task starts at start_time
        self.assertEqual(schedule[0]['start_time'], start_time)
        
        # Check that tasks are in the same order as sorted by priority
        self.assertEqual(schedule[0]['task'].title, "Task 1")
        self.assertEqual(schedule[1]['task'].title, "Task 2")
    
    def test_schedule_respects_duration_limits(self):
        tasks = [
            Task("Long Task", "", 3, 180, datetime.now() + timedelta(hours=1)),
            Task("Short Task", "", 2, 60, datetime.now() + timedelta(hours=2))
        ]
        
        self.mock_priority_engine.sort_by_priority.return_value = tasks
        
        start_time = datetime.now()
        short_duration = 120  # 2 hours
        
        schedule = self.scheduler.generate_schedule(tasks, start_time, short_duration)
        
        # Only the first task should fit in a 2-hour window
        self.assertEqual(len(schedule), 1)
        self.assertEqual(schedule[0]['task'].title, "Long Task")
    
    def test_empty_task_list(self):
        schedule = self.scheduler.generate_schedule([], datetime.now(), 120)
        self.assertEqual(len(schedule), 0)

if __name__ == '__main__':
    unittest.main()