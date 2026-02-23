import unittest
from datetime import datetime, timedelta
from product_idea.src.core.task import Task

class TestTask(unittest.TestCase):
    
    def setUp(self):
        self.task = Task(
            title="Test Task",
            description="Test Description",
            priority=2,
            estimated_time=60,
            deadline=datetime.now() + timedelta(days=1)
        )
    
    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "Test Description")
        self.assertEqual(self.task.priority, 2)
        self.assertEqual(self.task.estimated_time, 60)
        self.assertFalse(self.task.completed)
    
    def test_complete_task(self):
        self.task.complete()
        self.assertTrue(self.task.completed)
        self.assertIsNotNone(self.task.completed_at)
    
    def test_task_priority_levels(self):
        low_task = Task("Low", "", 1, 30)
        medium_task = Task("Medium", "", 2, 30)
        high_task = Task("High", "", 3, 30)
        
        self.assertEqual(low_task.priority, 1)
        self.assertEqual(medium_task.priority, 2)
        self.assertEqual(high_task.priority, 3)
    
    def test_task_string_representation(self):
        self.assertIn("Test Task", str(self.task))
        self.assertIn("Priority: 2", str(self.task))

if __name__ == '__main__':
    unittest.main()