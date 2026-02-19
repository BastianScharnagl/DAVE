import os
import json
from datetime import datetime
from typing import Dict, Any

def backup_memory() -> str:
    """Create a backup of all memory files

    Returns:
        str: JSON with backup status
    """
    try:
        # Ensure backup directory exists
        backup_dir = 'memory/backups'
        os.makedirs(backup_dir, exist_ok=True)
        
        # Timestamp for backup
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = f'{backup_dir}/{backup_name}'
        os.makedirs(backup_path, exist_ok=True)
        
        # Memory files to backup
        memory_files = ['context.md', 'database.md', 'messages.md']
        backup_manifest = {
            'backup_name': backup_name,
            'timestamp': datetime.now().isoformat(),
            'files': {}
        }
        
        # Copy each memory file
        for file_name in memory_files:
            source_path = f'memory/{file_name}'
            dest_path = f'{backup_path}/{file_name}'
            
            if os.path.exists(source_path):
                with open(source_path, 'r', encoding='utf-8') as src:
                    content = src.read()
                    
                with open(dest_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                    
                # Record file info
                backup_manifest['files'][file_name] = {
                    'size': len(content),
                    'last_modified': datetime.fromtimestamp(os.path.getmtime(source_path)).isoformat()
                }
            
        # Create manifest file
        manifest_path = f'{backup_path}/manifest.json'
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(backup_manifest, f, indent=2)
        
        return json.dumps({
            'status': 'success',
            'message': f'Backup created successfully: {backup_name}',
            'backup_name': backup_name,
            'path': backup_path,
            'file_count': len(backup_manifest['files']),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })

def restore_backup(backup_name: str) -> str:
    """Restore memory from a backup

    Args:
        backup_name (str): The name of the backup to restore

    Returns:
        str: JSON with restore status
    """
    try:
        backup_path = f'memory/backups/{backup_name}'
        
        # Check if backup exists
        if not os.path.exists(backup_path):
            return json.dumps({
                'status': 'error',
                'message': f'Backup not found: {backup_name}',
                'timestamp': datetime.now().isoformat()
            })
        
        # Check for manifest
        manifest_path = f'{backup_path}/manifest.json'
        if not os.path.exists(manifest_path):
            return json.dumps({
                'status': 'error',
                'message': f'Manifest not found in backup: {backup_name}',
                'timestamp': datetime.now().isoformat()
            })
        
        # Load manifest
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Restore each file
        restore_manifest = {
            'backup_name': backup_name,
            'restore_time': datetime.now().isoformat(),
            'restored_files': {}
        }
        
        for file_name in manifest['files'].keys():
            source_path = f'{backup_path}/{file_name}'
            dest_path = f'memory/{file_name}'
            
            if os.path.exists(source_path):
                with open(source_path, 'r', encoding='utf-8') as src:
                    content = src.read()
                    
                with open(dest_path, 'w', encoding='utf-8') as dst:
                    dst.write(content)
                    
                restore_manifest['restored_files'][file_name] = {
                    'size': len(content),
                    'restored_at': datetime.now().isoformat()
                }
            
        return json.dumps({
            'status': 'success',
            'message': f'Backup restored successfully: {backup_name}',
            'backup_name': backup_name,
            'files_restored': len(restore_manifest['restored_files']),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })

def list_backups() -> str:
    """List all available backups

    Returns:
        str: JSON with list of backups
    """
    try:
        backup_dir = 'memory/backups'
        
        if not os.path.exists(backup_dir):
            return json.dumps({
                'status': 'success',
                'backups': [],
                'count': 0,
                'timestamp': datetime.now().isoformat()
            })
        
        # List all backup directories
        backup_dirs = [d for d in os.listdir(backup_dir) if os.path.isdir(f'{backup_dir}/{d}') and d.startswith('backup_')]
        backups = []
        
        for backup_dir_name in sorted(backup_dirs, reverse=True):  # Most recent first
            backup_path = f'{backup_dir}/{backup_dir_name}'
            manifest_path = f'{backup_path}/manifest.json'
            
            backup_info = {
                'name': backup_dir_name,
                'path': backup_path
            }
            
            # Try to read manifest for additional info
            if os.path.exists(manifest_path):
                try:
                    with open(manifest_path, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                        backup_info['timestamp'] = manifest['timestamp']
                        backup_info['file_count'] = len(manifest['files'])
                except:
                    backup_info['timestamp'] = 'unknown'
                    backup_info['file_count'] = 'unknown'
            else:
                backup_info['timestamp'] = 'unknown'
                backup_info['file_count'] = 'unknown'
                
            backups.append(backup_info)
        
        return json.dumps({
            'status': 'success',
            'backups': backups,
            'count': len(backups),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return json.dumps({
            'status': 'error',
            'message': str(e),
            'timestamp': datetime.now().isoformat()
        })