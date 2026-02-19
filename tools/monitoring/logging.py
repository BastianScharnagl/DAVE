import os
import json
from datetime import datetime
from typing import Dict, Any

def log_event(level: str, message: str, source: str = "system", metadata: Dict = None) -> str:
    """Log an event to the system logs

    Args:
        level (str): The severity level (info, warning, error, debug)
        message (str): The log message
        source (str): The source of the event
        metadata (Dict): Additional context information

    Returns:
        str: JSON with log status
    """
    try:
        # Ensure logs directory exists
        logs_dir = 'memory/logs'
        os.makedirs(logs_dir, exist_ok=True)
        
        # Timestamp for log entry
        timestamp = datetime.now().isoformat()
        
        # Create log entry
        log_entry = {
            'id': _get_next_log_id(),
            'level': level.lower(),
            'message': message,
            'timestamp': timestamp,
            'source': source,
            'metadata': metadata or {}
        }
        
        # Determine log file (daily logs)
        date_str = datetime.now().strftime('%Y%m%d')
        log_file = f'{logs_dir}/system_{date_str}.log'
        
        # Append to log file
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        return json.dumps({
            'status': 'success',
            'message': 'Log entry created',
            'log_id': log_entry['id'],
            'timestamp': timestamp
        })
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })

def _get_next_log_id() -> int:
    """Get the next available log ID

    Returns:
        int: The next log ID
    """
    try:
        logs_dir = 'memory/logs'
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('system_') and f.endswith('.log')]
        
        # If no log files, start with 1
        if not log_files:
            return 1
        
        # Check all log files for the highest ID
        max_id = 0
        for log_file in log_files:
            file_path = f'{logs_dir}/{log_file}'
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                log_entry = json.loads(line.strip())
                                if log_entry['id'] > max_id:
                                    max_id = log_entry['id']
                            except:
                                continue
        
        return max_id + 1
        
    except:
        # Fallback to reading from database if available
        return 1

def get_system_logs(level: str = None, source: str = None, days: int = 7) -> str:
    """Retrieve system logs

    Args:
        level (str): Filter by level (info, warning, error, debug)
        source (str): Filter by source
        days (int): Number of days to look back

    Returns:
        str: JSON with logs
    """
    try:
        logs_dir = 'memory/logs'
        
        if not os.path.exists(logs_dir):
            return json.dumps({
                'status': 'success',
                'logs': [],
                'count': 0,
                'filters': {
                    'level': level,
                    'source': source,
                    'days': days
                }
            })
        
        # Determine date range
        from datetime import timedelta
        start_date = datetime.now() - timedelta(days=days)
        
        logs = []
        
        # Read all relevant log files
        log_files = [f for f in os.listdir(logs_dir) if f.startswith('system_') and f.endswith('.log')]
        
        for log_file in log_files:
            # Extract date from filename (system_YYYYMMDD.log)
            try:
                file_date_str = log_file.split('_')[1].split('.')[0]
                file_date = datetime.strptime(file_date_str, '%Y%m%d')
                
                # Skip if outside date range
                if file_date < start_date:
                    continue
                
                file_path = f'{logs_dir}/{log_file}'
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            try:
                                log_entry = json.loads(line.strip())
                                
                                # Apply filters
                                if level and log_entry['level'] != level.lower():
                                    continue
                                if source and log_entry['source'] != source:
                                    continue
                                
                                logs.append(log_entry)
                            except:
                                continue
            
            except:
                continue
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return json.dumps({
            'status': 'success',
            'logs': logs,
            'count': len(logs),
            'filters': {
                'level': level,
                'source': source,
                'days': days
            }
        })
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })