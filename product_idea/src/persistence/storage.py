"""
Storage module for Smart Task Optimizer
Implements persistent data storage for tasks and user preferences
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class PersistentStorage:
    """Handles persistent storage of tasks, user preferences, and model state"""
    
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        self.tasks_file = os.path.join(storage_dir, "tasks.json")
        self.settings_file = os.path.join(storage_dir, "settings.json")
        self.model_state_file = os.path.join(storage_dir, "model_state.json")
        
        # Ensure storage directory exists
        os.makedirs(storage_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self._init_data_files()
    
    def _init_data_files(self):
        """Initialize data files with default content if they don't exist"""
        # Initialize tasks file
        if not os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'w') as f:
                json.dump({
                    'tasks': [],
                    'created_at': datetime.now().isoformat()
                }, f, indent=2)
        
        # Initialize settings file
        if not os.path.exists(self.settings_file):
            with open(self.settings_file, 'w') as f:
                json.dump({
                    'default_priority_weights': {
                        'priority': 0.4,
                        'urgency': 0.3,
                        'effort': 0.2,
                        'value': 0.1
                    },
                    'user_preferences': {
                        'work_hours_start': 9,
                        'work_hours_end': 17,
                        'preferred_days': [0, 1, 2, 3, 4],  # Monday to Friday
                        'notification_preferences': {
                            'email': False,
                            'desktop': True,
                            'mobile': True
                        }
                    }
                }, f, indent=2)
        
        # Initialize model state file
        if not os.path.exists(self.model_state_file):
            with open(self.model_state_file, 'w') as f:
                json.dump({
                    'model_version': '1.0',
                    'last_trained': None,
                    'training_samples': 0,
                    'accuracy': 0.0,
                    'user_behavior_patterns': {}
                }, f, indent=2)
    
    def save_tasks(self, tasks: List[Dict]) -> bool:
        """Save tasks to persistent storage"""
        try:
            # Convert tasks to serializable format
            serializable_tasks = []
            for task in tasks:
                task_data = task.copy()
                # Convert datetime objects to ISO format strings
                if 'deadline' in task_data and task_data['deadline']:
                    task_data['deadline'] = task_data['deadline'].isoformat()
                if 'created_at' in task_data and task_data['created_at']:
                    task_data['created_at'] = task_data['created_at'].isoformat()
                if 'updated_at' in task_data and task_data['updated_at']:
                    task_data['updated_at'] = task_data['updated_at'].isoformat()
                if 'completed_at' in task_data and task_data['completed_at']:
                    task_data['completed_at'] = task_data['completed_at'].isoformat()
                serializable_tasks.append(task_data)
            
            data = {
                'tasks': serializable_tasks,
                'updated_at': datetime.now().isoformat()
            }
            
            with open(self.tasks_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving tasks: {e}")
            return False
    
    def load_tasks(self) -> List[Dict]:
        """Load tasks from persistent storage"""
        try:
            if not os.path.exists(self.tasks_file):
                return []
            
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
            
            tasks = []
            for task_data in data.get('tasks', []):
                # Convert ISO format strings back to datetime objects
                task = task_data.copy()
                if 'deadline' in task and task['deadline']:
                    task['deadline'] = datetime.fromisoformat(task['deadline'])
                if 'created_at' in task and task['created_at']:
                    task['created_at'] = datetime.fromisoformat(task['created_at'])
                if 'updated_at' in task and task['updated_at']:
                    task['updated_at'] = datetime.fromisoformat(task['updated_at'])
                if 'completed_at' in task and task['completed_at']:
                    task['completed_at'] = datetime.fromisoformat(task['completed_at'])
                tasks.append(task)
            
            return tasks
        except Exception as e:
            print(f"Error loading tasks: {e}")
            return []
    
    def save_settings(self, settings: Dict) -> bool:
        """Save user settings to persistent storage"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def load_settings(self) -> Dict:
        """Load user settings from persistent storage"""
        try:
            if not os.path.exists(self.settings_file):
                return {}
            
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {}
    
    def save_model_state(self, model_state: Dict) -> bool:
        """Save model state to persistent storage"""
        try:
            with open(self.model_state_file, 'w') as f:
                json.dump(model_state, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving model state: {e}")
            return False
    
    def load_model_state(self) -> Dict:
        """Load model state from persistent storage"""
        try:
            if not os.path.exists(self.model_state_file):
                return {}
            
            with open(self.model_state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading model state: {e}")
            return {}