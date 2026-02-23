"""
Priority Engine for Smart Task Optimizer
Implements the core algorithm for task prioritization
"""

class PriorityEngine:
    """Handles task prioritization based on multiple factors"""
    
    def __init__(self):
        # Base weights for different factors
        self.weights = {
            'priority': 0.4,
            'urgency': 0.3,
            'effort': 0.2,
            'value': 0.1
        }
    
    def calculate_urgency(self, task, current_time=None):
        """Calculate urgency score based on deadline"""
        import datetime
        
        if not task.deadline:
            return 1.0  # Default urgency if no deadline
            
        if current_time is None:
            current_time = datetime.datetime.now()
            
        # Time remaining in days
        time_remaining = (task.deadline - current_time).total_seconds() / (24 * 3600)
        
        # Higher urgency as deadline approaches
        if time_remaining <= 1:
            return 5.0
        elif time_remaining <= 3:
            return 4.0
        elif time_remaining <= 7:
            return 3.0
        elif time_remaining <= 14:
            return 2.0
        else:
            return 1.0

    def calculate_value(self, task):
        """Calculate value score based on priority and tags"""
        # Base value from priority
        value = task.priority
        
        # Bonus for important tags
        important_tags = ['important', 'critical', 'urgent', 'high-value']
        for tag in task.tags:
            if tag.lower() in important_tags:
                value += 1
                
        return min(value, 5)  # Cap at 5
    
    def calculate_score(self, task, current_time=None):
        """Calculate overall priority score for a task"""
        if task.completed:
            return 0.0
            
        urgency = self.calculate_urgency(task, current_time)
        value = self.calculate_value(task)
        
        # Effort is inverse - lower effort tasks are more attractive
        effort_factor = (6 - task.effort)  # 5->1, 4->2, 3->3, 2->4, 1->5
        
        # Weighted sum
        score = (
            self.weights['priority'] * task.priority +
            self.weights['urgency'] * urgency +
            self.weights['effort'] * effort_factor +
            self.weights['value'] * value
        )
        
        return round(score, 2)
    
    def rank_tasks(self, tasks, current_time=None):
        """Return tasks ranked by priority score"""
        scored_tasks = [
            (task, self.calculate_score(task, current_time))
            for task in tasks
        ]
        
        # Sort by score descending
        ranked = sorted(scored_tasks, key=lambda x: x[1], reverse=True)
        return ranked