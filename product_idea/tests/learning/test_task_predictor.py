import unittest
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import Mock

# Import our classes
from product_idea.src.core.task import Task
from product_idea.src.learning.task_predictor import TaskPredictor

class TestTaskPredictor(unittest.TestCase):
    
    def setUp(self):
        self.predictor = TaskPredictor()
        
        # Create test tasks
        self.task1 = Task(
            title="Urgent Task",
            priority=5,
            effort=3,
            deadline=datetime.now() + timedelta(hours=2)
        )
        
        self.task2 = Task(
            title="Low Priority Task",
            priority=2,
            effort=2,
            deadline=datetime.now() + timedelta(days=7)
        )
        
    def test_feature_extraction(self):
        # Test that feature extraction works correctly
        features = self.predictor.extract_features(self.task1)
        
        # Check shape
        self.assertEqual(features.shape, (1, 8))
        
        # Check that priority is in correct position
        self.assertEqual(features[0][0], 5)  # Priority
        self.assertEqual(features[0][1], 3)  # Effort
        
        # Check that urgency is high for near deadline
        self.assertGreater(features[0][2], 4)  # Urgency should be high

    def test_predict_optimal_time_untrained(self):
        # Test prediction when model is not trained
        start_time = datetime.now()
        end_time = start_time + timedelta(hours=4)
        
        optimal_time = self.predictor.predict_optimal_time(
            self.task1, start_time, end_time
        )
        
        # Should return middle of window when untrained
        expected = start_time + (end_time - start_time) / 2
        # Allow for small differences
        self.assertAlmostEqual(
            (optimal_time - expected).total_seconds(), 
            0, 
            delta=60  # 60 second tolerance
        )
        
    def test_train_model(self):
        # Create mock historical data
        historical_data = []
        base_time = datetime.now()
        
        for i in range(100):
            task = Task(
                title=f"Task {i}",
                priority=np.random.randint(1, 6),
                effort=np.random.randint(1, 6),
                deadline=base_time + timedelta(days=np.random.randint(1, 14))
            )
            
            # Create record
            record = {
                'task': task,
                'scheduled_start': base_time + timedelta(hours=i),
                'actual_start': base_time + timedelta(hours=i + np.random.choice([0, 1])),
                'completed': np.random.choice([True, False], p=[0.7, 0.3])
            }
            historical_data.append(record)
        
        # Train model
        result = self.predictor.train(historical_data)
        
        # Check that training completed
        self.assertTrue(self.predictor.is_trained)
        self.assertIn('accuracy', result)
        self.assertIn('samples', result)
        self.assertEqual(result['samples'], 100)
        
    def test_save_and_load_model(self):
        # Create a temporary model path
        self.predictor.model_path = 'test_model.pkl'
        
        # Train a simple model
        historical_data = []
        base_time = datetime.now()
        
        for i in range(10):
            task = Task(
                title=f"Task {i}",
                priority=3,
                effort=3,
                deadline=base_time + timedelta(days=7)
            )
            
            record = {
                'task': task,
                'scheduled_start': base_time + timedelta(hours=i),
                'actual_start': base_time + timedelta(hours=i),
                'completed': True
            }
            historical_data.append(record)
        
        # Train and save
        self.predictor.train(historical_data)
        
        # Create new predictor and load
        new_predictor = TaskPredictor('test_model.pkl')
        loaded = new_predictor.load_model()
        
        self.assertTrue(loaded)
        self.assertTrue(new_predictor.is_trained)
        
        # Clean up
        import os
        if os.path.exists('test_model.pkl'):
            os.remove('test_model.pkl')