import unittest
from datetime import datetime, timedelta
from product_idea.src.core.task import Task
from product_idea.src.core.priority_engine import PriorityEngine

class TestPriorityEngine(unittest.TestCase):
    
    def setUp(self):
        self.engine = PriorityEngine()
        self.tasks = [
            Task("Urgent & Important", "", 3, 60, datetime.now() + timedelta(hours=1)),
            Task("Important", "", 3, 120, datetime.now() + timedelta(days=3)),
            Task("Urgent", "", 2, 30, datetime.now() + timedelta(hours=2)),
            Task("Low Priority", "", 1, 45, datetime.now() + timedelta(weeks=1))
        ]
    
    def test_priority_scoring(self):
        scores = [self.engine.calculate_priority_score(task) for task in self.tasks]
        
        # Urgent & Important should have highest score
        self.assertEqual(max(scores), scores[0])
        
        # Low Priority should have lowest score
        self.assertEqual(min(scores), scores[3])
    
    def test_sort_tasks_by_priority(self):
        sorted_tasks = self.engine.sort_by_priority(self.tasks)
        
        # Most urgent/important should be first
        self.assertEqual(sorted_tasks[0].title, "Urgent & Important")
        
        # Least important should be last
        self.assertEqual(sorted_tasks[-1].title, "Low Priority")
    
    def test_deadline_impact_on_priority(self):
        # Two tasks with same priority but different deadlines
        task1 = Task("Same Priority", "", 2, 60, datetime.now() + timedelta(hours=1))
        task2 = Task("Same Priority", "", 2, 60, datetime.now() + timedelta(days=2))
        
        score1 = self.engine.calculate_priority_score(task1)
        score2 = self.engine.calculate_priority_score(task2)
        
        # Task with sooner deadline should have higher score
        self.assertGreater(score1, score2)

if __name__ == '__main__':
    unittest.main()