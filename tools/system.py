import os
import json
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional

def list_directory_contents(path: str) -> str:
    """List the contents of a directory

    Args:
        path (str): The path to the directory

    Returns:
        str: The contents of the directory
    """
    try:
        contents = os.listdir(path)
        return json.dumps({
            'path': path,
            'contents': contents,
            'total_items': len(contents)
        })
    except FileNotFoundError:
        return json.dumps({
            'error': f'Directory not found: {path}',
            'path': path
        })
    except PermissionError:
        return json.dumps({
            'error': f'Permission denied: {path}',
            'path': path
        })

def read_file(path: str) -> str:
    """Read the contents of a file

    Args:
        path (str): The path to the file

    Returns:
        str: The contents of the file or error message
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return json.dumps({
            'path': path,
            'content': content,
            'size': len(content),
            'modified': datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
        })
    except FileNotFoundError:
        return json.dumps({
            'error': f'File not found: {path}',
            'path': path
        })
    except PermissionError:
        return json.dumps({
            'error': f'Permission denied: {path}',
            'path': path
        })
    except UnicodeDecodeError:
        return json.dumps({
            'error': f'Unicode decode error: {path}',
            'path': path
        })

def write_file(path: str, content: str) -> str:
    """Write the contents of a file

    Args:
        path (str): The path to the file
        content (str): The contents of the file

    Returns:
        str: Success message with file details or error message
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return json.dumps({
            'message': 'File written successfully',
            'path': path,
            'size': len(content),
            'modified': datetime.now().isoformat()
        })
    except PermissionError:
        return json.dumps({
            'error': f'Permission denied: {path}',
            'path': path
        })
    except OSError as e:
        return json.dumps({
            'error': f'OS error occurred: {str(e)}',
            'path': path
        })

def delete_file(path: str) -> str:
    """Delete a file

    Args:
        path (str): The path to the file

    Returns:
        str: Success message or error message
    """
    try:
        if not os.path.exists(path):
            return json.dumps({
                'error': f'File does not exist: {path}',
                'path': path
            })
            
        if os.path.isfile(path):
            response = input("Are you sure you want to delete this file? (y/n)").strip().lower()
            if response == "y" or response == "yes":
                os.remove(path)
                return json.dumps({
                    'message': 'File deleted successfully',
                    'path': path
                })
            else:
                return json.dumps({
                    'message': 'File not deleted',
                    'path': path
                })
        else:
            return json.dumps({
                'error': f'Path is not a file: {path}',
                'path': path
            })
    except PermissionError:
        return json.dumps({
            'error': f'Permission denied: {path}',
            'path': path
        })
    except OSError as e:
        return json.dumps({
            'error': f'OS error occurred: {str(e)}',
            'path': path
        })

def create_directory(path: str) -> str:
    """Create a directory and any parent directories if needed

    Args:
        path (str): The path to the directory

    Returns:
        str: Success message or error message
    """
    try:
        os.makedirs(path, exist_ok=True)
        return json.dumps({
            'message': 'Directory created successfully',
            'path': path
        })
    except PermissionError:
        return json.dumps({
            'error': f'Permission denied: {path}',
            'path': path
        })
    except OSError as e:
        return json.dumps({
            'error': f'OS error occurred: {str(e)}',
            'path': path
        })

def file_exists(path: str) -> str:
    """Check if a file exists

    Args:
        path (str): The path to the file

    Returns:
        str: JSON with existence status
    """
    return json.dumps({
        'path': path,
        'exists': os.path.exists(path),
        'is_file': os.path.isfile(path),
        'is_directory': os.path.isdir(path)
    })

def restart():
    """Restart"""
    print("argv was", sys.argv)
    print("sys.executable was", sys.executable)
    print("os.getcwd() was", os.getcwd())
    print("restart now")

    os.chdir(os.getcwd())
    if os.path.exists(sys.executable):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        os.execv("/usr/bin/python3", ['python'] + sys.argv)

def run_command(command: str) -> str:
    """Run a command and return the output

    Args:
        command (str): The command to run

    Returns:
        str: JSON with output or error
    """
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        return json.dumps({
            'output': output,
            'success': True
        })
    except subprocess.CalledProcessError as e:
        return json.dumps({
            'error': str(e),
            'success': False
        })