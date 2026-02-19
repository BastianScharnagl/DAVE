import os
import json
import sys
import subprocess
from datetime import datetime
from typing import Dict, List, Any, Optional

def file_exists(path: str) -> str:
    """Check if a file exists

    Args:
        path (str): The path to the file

    Returns:
        str: Existence status
    """
    if os.path.isfile(path):
        return f'File {path} exists.'
    else:
        return f'File {path} does not exist.'

def read_file(path: str) -> str:
    """Read the contents of a file

    Args:
        path (str): The path to the file

    Returns:
        str: Contents of the file
    """
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content
    
def write_file(path: str, content: str) -> str:
    """Write the contents of a file

    Args:
        path (str): The path to the file
        content (str): The contents of the file

    Returns:
        str: Status message
    """
    user_input = input("Are you sure you want to write this file? (y/n)").strip().lower()
    if user_input != "y":
        return f'User denied tool write_file {path}'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
            
    return f'File {path} written successfully.'

def delete_file(path: str) -> str:
    """Delete a file

    Args:
        path (str): The path to the file

    Returns:
        str: Status message
    """
    user_input = input("Are you sure you want to delete this file? (y/n)").strip().lower()
    if user_input != "y":
        return f'User denied tool delete_file {path}'
    
    os.remove(path)
    return f'File {path} deleted successfully.'

def read_directory(path: str) -> str:
    """List the contents of a directory

    Args:
        path (str): The path to the directory

    Returns:
        str: Existence status
    """
    if os.path.isdir(path):
        return f'Directory {path} exists.'
    else:
        return f'Directory {path} does not exist.'


def create_directory(path: str) -> str:
    """Create a directory and any parent directories if needed

    Args:
        path (str): The path to the directory

    Returns:
        str: Status message
    """
    user_input = input("Are you sure you want to create this directory? (y/n)").strip().lower()
    if user_input != "y":
        return f'User denied tool create_directory {path}'
    
    os.makedirs(path, exist_ok=True)
    return f'Directory {path} created successfully.'

def run_command(command: str) -> str:
    """Run a command and return the output

    Args:
        command (str): The command to run

    Returns:
        str: Status message
    """
    user_input = input("Are you sure you want to run this command? (y/n)").strip().lower()
    if user_input != "y":
        return f'User denied tool run_command {command}'

    output = subprocess.check_output(command, shell=True, text=True)
    return f'Command {command} executed with output: {output}'

def restart():
    """Restart the agent

    Returns:
        str: Status message
    """
    user_input = input("Are you sure you want to restart the agent? (y/n)").strip().lower()
    if user_input != "y":
        return f'User denied tool restart'

    os.chdir(os.getcwd())
    if os.path.exists(sys.executable):
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        os.execv("/usr/bin/python3", ['python'] + sys.argv)

    return f'Agent restarted successfully.'