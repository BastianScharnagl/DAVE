"""
Tests for the CLI module
"""

import unittest
import sys
import io
from unittest.mock import patch
from datetime import datetime, timedelta
from product_idea.src.cli.cli import TaskCLI


class TestTaskCLI(unittest.TestCase):
    """Test the command-line interface"""
    
    def setUp(self):
        self.cli = TaskCLI()
        
        # Add some test tasks
        self.cli.add_task("Urgent Task", priority=5, effort=3, 
                         deadline=datetime.now() + timedelta(hours=2))
        self.cli.add_task("Important Task", priority=4, effort=4, 
                         deadline=datetime.now() + timedelta(days=2))
        self.cli.add_task("Low Priority Task", priority=1, effort=2)
    
    def test_add_task(self):
        """Test adding a task"""
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cli.add_task("Test Task", priority=3, effort=2)
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        # Check output
        output = captured_output.getvalue()
        self.assertIn("✓ Added task: [3] Test Task (Effort: 2)", output)
        
        # Check task was added
        self.assertEqual(len(self.cli.tasks), 4)
        self.assertEqual(self.cli.tasks[3].title, "Test Task")
    
    def test_list_tasks(self):
        """Test listing tasks"""
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cli.list_tasks()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Check header
        self.assertIn("ID", output)
        self.assertIn("Priority", output)
        self.assertIn("Title", output)
        
        # Check tasks are listed
        self.assertIn("Urgent Task", output)
        self.assertIn("Important Task", output)
        self.assertIn("Low Priority Task", output)
        
        # Check priority scores are shown
        self.assertRegex(output, r"\d+\.\d")  # Should contain decimal scores
    
    def test_schedule_day(self):
        """Test generating a daily schedule"""
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        self.cli.schedule_day()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        
        # Check schedule header
        self.assertIn("Schedule for", output)
        self.assertIn("─", output)
        
        # Check tasks are scheduled
        self.assertIn("Urgent Task", output)
        self.assertIn("Important Task", output)
        
        # Check time format
        self.assertRegex(output, r"\d{2}:\d{2} - \d{2}:\d{2}")
    
    def test_empty_schedule(self):
        """Test scheduling with no tasks"""
        cli = TaskCLI()  # Fresh CLI with no tasks
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        cli.schedule_day()
        
        # Reset stdout
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn("No active tasks to schedule.", output)