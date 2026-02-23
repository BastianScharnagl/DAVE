"""
Machine learning model for task prioritization
"""

import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import json
import os
from datetime import datetime

class TaskPrioritizationModel:
    """
    ML model that learns user task prioritization patterns
    """
    
    def __init__(self, model_path=None):
        self.model_path = model_path or 'task_model.pkl'
        self.scaler_path = model_path.replace('.pkl', '_scaler.pkl') if model_path else 'scaler.pkl'
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.feature_names = [
            'urgency_score',
            'importance_score',
            'estimated_duration',
            'time_of_day',
            'day_of_week',
            'completion_rate',
            'streak_count',
            'category_frequency'
        ]
        self.is_trained = False
        
        # Load model if it exists
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            self.load_model()
    
    def extract_features(self, task_data):
        """
        Extract features from task data for model input
        
        Args:
            task_data (dict): Task information
            
        Returns:
            np.array: Feature vector
        """
        # Time-based features
        now = datetime.now()
        time_of_day = now.hour + now.minute / 60
        day_of_week = now.weekday()
        
        # Historical performance features (mock data for now)
        completion_rate = 0.75  # Average completion rate
        streak_count = 5  # Current productivity streak
        
        # Category frequency (how often this category appears)
        category_frequency = 0.3
        
        features = [
            task_data.get('urgency_score', 0),
            task_data.get('importance_score', 0),
            task_data.get('estimated_duration', 30),
            time_of_day,
            day_of_week,
            completion_rate,
            streak_count,
            category_frequency
        ]
        
        return np.array(features).reshape(1, -1)
    
    def train(self, training_data, labels):
        """
        Train the model on task data
        
        Args:
            training_data (list): List of task dictionaries
            labels (list): True priority labels (0-3 scale)
        """
        # Extract features from training data
        X = np.array([self.extract_features(task) for task in training_data])
        X = X.reshape(len(training_data), -1)  # Flatten features
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, labels)
        self.is_trained = True
        
        # Save model
        self.save_model()
        
    def predict_priority(self, task_data):
        """
        Predict priority score for a task
        
        Args:
            task_data (dict): Task information
            
        Returns:
            int: Predicted priority (0-3 scale)
        """
        if not self.is_trained:
            # Default priority logic if model not trained
            urgency = task_data.get('urgency_score', 0)
            importance = task_data.get('importance_score', 0)
            score = (urgency * 0.6) + (importance * 0.4)
            
            if score >= 0.7:
                return 3  # High priority
            elif score >= 0.4:
                return 2  # Medium priority
            elif score >= 0.2:
                return 1  # Low priority
            else:
                return 0  # Ignore
        
        # Use trained model
        features = self.extract_features(task_data)
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        
        return int(prediction)
    
    def predict_proba(self, task_data):
        """
        Predict probability distribution across priority levels
        
        Args:
            task_data (dict): Task information
            
        Returns:
            dict: Probability distribution
        """
        if not self.is_trained:
            return {0: 0.1, 1: 0.2, 2: 0.3, 3: 0.4}  # Default distribution
        
        features = self.extract_features(task_data)
        features_scaled = self.scaler.transform(features)
        proba = self.model.predict_proba(features_scaled)[0]
        
        return {i: float(proba[i]) for i in range(len(proba))}
    
    def save_model(self):
        """
        Save the trained model and scaler
        """
        joblib.dump(self.model, self.model_path)
        joblib.dump(self.scaler, self.scaler_path)
    
    def load_model(self):
        """
        Load the trained model and scaler
        """
        self.model = joblib.load(self.model_path)
        self.scaler = joblib.load(self.scaler_path)
        self.is_trained = True
    
    def get_feature_importance(self):
        """
        Get feature importance scores
        
        Returns:
            dict: Feature names and importance scores
        """
        if not self.is_trained:
            return {name: 0.1 for name in self.feature_names}
        
        importance = self.model.feature_importances_
        return {name: float(importance[i]) for i, name in enumerate(self.feature_names)}
