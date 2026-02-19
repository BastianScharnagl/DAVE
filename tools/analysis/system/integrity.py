import os
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Any

def check_system_integrity() -> str:
    """Perform comprehensive system integrity check

    Returns:
        str: JSON with integrity check results
    """
    try:
        results = {
            'timestamp': datetime.now().isoformat(),
            'status': 'completed',
            'checks': {
                'directory_structure': _check_directory_structure(),
                'critical_files': _check_critical_files(),
                'file_permissions': _check_file_permissions(),
                'system_config': _check_system_config()
            }
        }
        
        # Determine overall status
        critical_failures = []
        for check_name, check_result in results['checks'].items():
            if check_result['status'] == 'failed':
                if check_name in ['directory_structure', 'critical_files', 'system_config']:
                    critical_failures.append(check_name)
        
        results['status'] = 'failed' if critical_failures else 'completed'
        
        return json.dumps(results, indent=2)
        
    except Exception as e:
        return json.dumps({
            'error': str(e),
            'timestamp': datetime.now().isoformat(),
            'status': 'error'
        })

def _check_directory_structure() -> Dict[str, Any]:
    """Check if required directories exist

    Returns:
        Dict[str, Any]: Check results
    """
    required_dirs = [
        './tools',
        './tools/agent',
        './tools/analysis',
        './tools/analysis/data',
        './tools/analysis/system',
        './tools/analysis/performance',
        './tools/analysis/health',
        './tools/management',
        './tools/monitoring',
        './memory',
        './memory/logs',
        './memory/backups'
    ]
    
    missing_dirs = []
    for directory in required_dirs:
        if not os.path.exists(directory):
            missing_dirs.append(directory)
    
    return {
        'status': 'failed' if missing_dirs else 'passed',
        'message': f'Missing directories: {missing_dirs}' if missing_dirs else 'All required directories exist',
        'missing': missing_dirs,
        'total_required': len(required_dirs),
        'found': len(required_dirs) - len(missing_dirs)
    }

def _check_critical_files() -> Dict[str, Any]:
    """Check if critical files exist and are accessible

    Returns:
        Dict[str, Any]: Check results
    """
    critical_files = [
        './interface.py',
        './config.py',
        './dave.py',
        './tools/system.py',
        './memory/context.md',
        './memory/database.md',
        './memory/messages.md',
        './memory/todo.md'
    ]
    
    missing_files = []
    inaccessible_files = []
    
    for file_path in critical_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            try:
                with open(file, 'r') as f:
                    pass
            except:
                inaccessible_files.append(file_path)
    
    status = 'passed'
    if missing_files:
        status = 'failed'
    elif inaccessible_files:
        status = 'warning'
    
    return {
        'status': status,
        'message': 'Critical files check completed',
        'missing': missing_files,
        'inaccessible': inaccessible_files,
        'total_critical': len(critical_files),
        'accessible': len(critical_files) - len(missing_files) - len(inaccessible_files)
    }

def _check_file_permissions() -> Dict[str, Any]:
    """Check file permissions for security

    Returns:
        Dict[str, Any]: Check results
    """
    # This is a simplified check - in production, you'd want more comprehensive security checks
    executable_files = [
        './interface.py',
        './dave.py'
    ]
    
    issues = []
    for file_path in executable_files:
        if os.path.exists(file_path):
            # Check if file is readable and writable by owner
            stat = os.stat(file_path)
            if not (stat.st_mode & 0o400):  # Read permission for owner
                issues.append(f'{file_path}: Missing read permission for owner')
            if not (stat.st_mode & 0o200):  # Write permission for owner
                issues.append(f'{file_path}: Missing write permission for owner')
    
    return {
        'status': 'warning' if issues else 'passed',
        'message': 'File permissions check completed',
        'issues': issues,
        'total_executable': len(executable_files)
    }

def _check_system_config() -> Dict[str, Any]:
    """Check system configuration

    Returns:
        Dict[str, Any]: Check results
    """
    try:
        import config
        # Trigger validation
        config.Config.validate()
        return {
            'status': 'passed',
            'message': 'System configuration is valid'
        }
    except Exception as e:
        return {
            'status': 'failed',
            'message': f'System configuration error: {str(e)}'
        }

def generate_integrity_report() -> str:
    """Generate a comprehensive integrity report

    Returns:
        str: Formatted integrity report
    """
    import json
    results = json.loads(check_system_integrity())
    
    report = f"""# System Integrity Report

**Generated:** {results['timestamp']}
**Overall Status:** {results['status'].upper()}

## Directory Structure
- Status: {results['checks']['directory_structure']['status'].upper()}
- Message: {results['checks']['directory_structure']['message']}

## Critical Files
- Status: {results['checks']['critical_files']['status'].upper()}
- Message: {results['checks']['critical_files']['message']}
- Missing: {len(results['checks']['critical_files']['missing'])}
- Inaccessible: {len(results['checks']['critical_files']['inaccessible'])}

## File Permissions
- Status: {results['checks']['file_permissions']['status'].upper()}
- Message: {results['checks']['file_permissions']['message']}
- Issues: {len(results['checks']['file_permissions']['issues'])}

## System Configuration
- Status: {results['checks']['system_config']['status'].upper()}
- Message: {results['checks']['system_config']['message']}

"""
    
    return report