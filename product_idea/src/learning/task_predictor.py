"""
Task Predictor module for Smart Task Optimizer
Implements machine learning model for user behavior prediction
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

class TaskPredictor:
    """Machine learning model to predict optimal task scheduling based on user behavior"""
    
    def __init__(self, model_path=None):
        self.model_path = model_path or 'task_predictor_model.pkl'
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def extract_features(self, task, current_time=None):
        """Extract features from task and context for prediction"""
        if current_time is None:
            current_time = datetime.now()
            
        # Time-based features
        hour = current_time.hour
        day_of_week = current_time.weekday()  # 0=Monday, 6=Sunday
        is_weekend = 1 if day_of_week >= 5 else 0
        
        # Task features
        priority = task.priority
        effort = task.effort
        has_deadline = 1 if task.deadline else 0
        
        # Time until deadline (in days)
        if task.deadline:
            time_until_deadline = (task.deadline - current_time).total_seconds() / (24 * 3600)
            urgency = min(time_until_deadline / 7, 5)  # Normalize to 0-5 scale
        else:
            time_until_deadline = 30  # Default
            urgency = 1
        
        # Create feature vector
        features = np.array([[
            priority,
            effort,
            urgency,
            has_deadline,
            hour,
            day_of_week,
            is_weekend,
            time_until_deadline
        ]])
        
        return features
    
    def predict_optimal_time(self, task, start_time, end_time):
        """Predict the optimal time to work on a task within a given time window"""
        if not self.is_trained:
            # If model isn't trained, return middle of window
            duration = (end_time - start_time) / 2
            return start_time + duration
            
        # Generate time slots
        time_slots = []
        current = start_time
        while current < end_time:
            time_slots.append(current)
            current += timedelta(minutes=30)
            
        # Predict suitability for each time slot
        predictions = []
        for slot in time_slots:
            features = self.extract_features(task, slot)
            # Predict probability of successful completion
            prob = self.model.predict_proba(features)[0][1]
            predictions.append((slot, prob))
            
        # Return time slot with highest probability
        optimal_time = max(predictions, key=lambda x: x[1])[0]
        return optimal_time
    
    def train(self, historical_data):
        """Train the model on historical task completion data"""
        # Convert historical data to features and labels
        features = []
        labels = []  # 1 if task was completed successfully, 0 if not
        
        for record in historical_data:
            task = record['task']
            start_time = record['scheduled_start']
            actual_start = record['actual_start']
            completed = record['completed']
            
            # Extract features
            feature_vec = self.extract_features(task, start_time).flatten()
            features.append(feature_vec)
            
            # Label: 1 if task was started within 30 mins of scheduled time AND completed
            timely_start = abs((actual_start - start_time).total_seconds()) <= 1800
            labels.append(1 if completed and timely_start else 0)
            
        X = np.array(features)
        y = np.array(labels)
        
        # Train the model
        self.model.fit(X, y)
        self.is_trained = True
        
        # Save the trained model
        self.save_model()
        
        return {"accuracy": self.model.score(X, y), "samples": len(y)}
    
    def save_model(self):
        """Save the trained model to disk"""
        joblib.dump(self.model, self.model_path)
    
    def load_model(self):
        """Load a trained model from disk"""
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            self.is_trained = True
            return True
        return False