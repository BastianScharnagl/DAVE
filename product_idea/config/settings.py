"""
Configuration settings for Smart Task Optimizer
"""

# Priority scoring weights
PRIORITY_WEIGHTS = {
    'urgency': 0.3,
    'importance': 0.4,
    'effort': 0.2,
    'deadline': 0.1
}

# Task categories
CATEGORIES = [
    'work',
    'personal',
    'health',
    'finance',
    'learning',
    'social'
]

# Default task properties
DEFAULT_TASK = {
    'status': 'pending',
    'priority_score': 0,
    'category': 'personal',
    'estimated_time': 30,  # minutes
    'created_at': None,
    'updated_at': None
}

# ML model configuration
MODEL_CONFIG = {
    'training_frequency': 'daily',
    'feature_set': ['time_of_day', 'day_of_week', 'task_category', 'duration', 'completion_rate'],
    'algorithm': 'random_forest',
    'confidence_threshold': 0.7
}

# Sync configuration
SYNC_CONFIG = {
    'enabled': True,
    'interval': 300,  # seconds
    'provider': 'dave_cloud',  # or 'google_drive', 'dropbox'
    'max_retries': 3
}

# UI configuration
UI_CONFIG = {
    'theme': 'dark',
    'notifications': True,
    'auto_suggest': True,
    'daily_review': True
}