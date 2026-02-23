import unittest
import tkinter as tk
from unittest.mock import patch, MagicMock

# Import the GUI class
import sys
sys.path.append('../gui')
from main import TaskOptimizerGUI

class TestTaskOptimizerGUI(unittest.TestCase):
    
    def setUp(self):
        self.root = tk.Tk()
        self.app = TaskOptimizerGUI(self.root)
    
    def tearDown(self):
        self.root.destroy()
    
    def test_add_task_with_valid_input(self):
        """Test adding a task with valid input"""
        # Set input values
        self.app.task_name.insert(0, "Test Task")
        self.app.priority_var.set("High")
        self.app.effort_var.set("7")
        self.app.deadline_var.set("2024-01-15")
        
        # Call add_task method
        self.app.add_task()
        
        # Check if task was added to the list
        tree_items = self.app.tree.get_children()
        self.assertEqual(len(tree_items), 1)
        
        # Check task details
        item_values = self.app.tree.item(tree_items[0])['values']
        self.assertEqual(item_values[0], "Test Task")
        self.assertEqual(item_values[1], "High")
        self.assertEqual(item_values[2], 7)
        self.assertEqual(item_values[3], "2024-01-15")
    
    def test_add_task_with_empty_name(self):
        """Test adding a task with empty name (should show warning)"""
        # Set empty name
        self.app.task_name.insert(0, "")
        
        # Mock messagebox.showwarning
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.app.add_task()
            
            # Check if warning was shown
            mock_warning.assert_called_once()
            
            # Check that no task was added
            tree_items = self.app.tree.get_children()
            self.assertEqual(len(tree_items), 0)
    
    def test_remove_task(self):
        """Test removing a selected task"""
        # Add a task first
        self.app.tasks = [{
            'name': 'Test Task',
            'priority': 'Medium',
            'effort': 5,
            'deadline': '2024-01-15',
            'completed': False,
            'score': 0,
            'scheduled_time': ''
        }]
        self.app.update_task_list()
        
        # Select the task
        items = self.app.tree.get_children()
        self.app.tree.selection_set(items[0])
        
        # Mock messagebox.askyesno to return True
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.remove_task()
            
            # Check that task list is empty
            tree_items = self.app.tree.get_children()
            self.assertEqual(len(tree_items), 0)
            
            # Check that task was removed from self.tasks
            self.assertEqual(len(self.app.tasks), 0)
    
    def test_mark_complete(self):
        """Test marking a task as complete"""
        # Add a task
        self.app.tasks = [{
            'name': 'Test Task',
            'priority': 'Medium',
            'effort': 5,
            'deadline': '2024-01-15',
            'completed': False,
            'score': 0,
            'scheduled_time': ''
        }]
        self.app.update_task_list()
        
        # Select the task
        items = self.app.tree.get_children()
        self.app.tree.selection_set(items[0])
        
        # Call mark_complete
        self.app.mark_complete()
        
        # Check that task is marked as complete
        self.assertTrue(self.app.tasks[0]['completed'])
        
        # Check that task is no longer in the treeview
        tree_items = self.app.tree.get_children()
        self.assertEqual(len(tree_items), 0)
    
    def test_calculate_priority_score_basic(self):
        """Test basic priority score calculation"""
        # Test Critical priority
        task = {'priority': 'Critical', 'effort': 5, 'deadline': ''}
        score = self.app.calculate_priority_score(task)
        self.assertGreater(score, 2)  # Should be higher than Medium priority
        
        # Test Low priority
        task = {'priority': 'Low', 'effort': 5, 'deadline': ''}
        score = self.app.calculate_priority_score(task)
        self.assertLess(score, 2)  # Should be lower than Medium priority
    
    def test_calculate_priority_score_deadline_urgency(self):
        """Test that deadline affects priority score"""
        # Task with same priority and effort, but different deadlines
        normal_task = {'priority': 'High', 'effort': 5, 'deadline': '2024-12-31'}
        urgent_task = {'priority': 'High', 'effort': 5, 'deadline': '2024-01-01'}  # Assuming this is soon
        
        normal_score = self.app.calculate_priority_score(normal_task)
        urgent_score = self.app.calculate_priority_score(urgent_task)
        
        # Urgent task should have higher score
        self.assertGreater(urgent_score, normal_score)
    
    def test_optimize_schedule(self):
        """Test that optimize_schedule sorts tasks by priority score"""
        # Add tasks with different priorities
        self.app.tasks = [
            {'name': 'Low Priority', 'priority': 'Low', 'effort': 5, 'deadline': '', 'completed': False, 'score': 0, 'scheduled_time': ''},
            {'name': 'High Priority', 'priority': 'High', 'effort': 5, 'deadline': '', 'completed': False, 'score': 0, 'scheduled_time': ''},
            {'name': 'Critical Priority', 'priority': 'Critical', 'effort': 5, 'deadline': '', 'completed': False, 'score': 0, 'scheduled_time': ''}
        ]
        
        self.app.update_task_list()
        
        # Mock messagebox.showinfo
        with patch('tkinter.messagebox.showinfo'):
            self.app.optimize_schedule()
            
            # Get items from treeview
            items = self.app.tree.get_children()
            item_values = [self.app.tree.item(item)['values'] for item in items]
            
            # Check that tasks are ordered by score (highest first)
            # Critical should be first, then High, then Low
            self.assertEqual(item_values[0][0], 'Critical Priority')
            self.assertEqual(item_values[1][0], 'High Priority')
            self.assertEqual(item_values[2][0], 'Low Priority')
    
    def test_generate_schedule(self):
        """Test that generate_schedule populates the schedule view"""
        # Add and schedule some tasks
        self.app.tasks = [
            {'name': 'Morning Task', 'priority': 'High', 'effort': 5, 'deadline': '', 'completed': False, 'score': 3.0, 'scheduled_time': '09:00'},
            {'name': 'Afternoon Task', 'priority': 'Medium', 'effort': 3, 'deadline': '', 'completed': False, 'score': 2.0, 'scheduled_time': '14:00'}
        ]
        
        self.app.update_task_list()
        
        # Call generate_schedule
        self.app.generate_schedule()
        
        # Check that schedule tree has items
        schedule_items = self.app.schedule_tree.get_children()
        self.assertEqual(len(schedule_items), 2)
        
        # Check order and values
        first_item = self.app.schedule_tree.item(schedule_items[0])['values']
        self.assertEqual(first_item[0], '09:00')
        self.assertEqual(first_item[1], 'Morning Task')
    
    def test_reset_tasks(self):
        """Test that reset_tasks clears all data"""
        # Add some tasks
        self.app.tasks = [
            {'name': 'Task 1', 'priority': 'Medium', 'effort': 5, 'deadline': '', 'completed': False, 'score': 0, 'scheduled_time': ''},
            {'name': 'Task 2', 'priority': 'High', 'effort': 3, 'deadline': '', 'completed': False, 'score': 0, 'scheduled_time': ''}
        ]
        self.app.update_task_list()
        
        # Mock messagebox.askyesno to return True
        with patch('tkinter.messagebox.askyesno', return_value=True):
            with patch('tkinter.messagebox.showinfo'):
                self.app.reset_tasks()
                
                # Check that tasks list is empty
                self.assertEqual(len(self.app.tasks), 0)
                
                # Check that treeview is empty
                tree_items = self.app.tree.get_children()
                self.assertEqual(len(tree_items), 0)
                
                # Check that schedule view is empty
                schedule_items = self.app.schedule_tree.get_children()
                self.assertEqual(len(schedule_items), 0)

if __name__ == '__main__':
    unittest.main()