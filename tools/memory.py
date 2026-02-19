import os

def read_memory(name: str) -> str:
    """Read a memory
    Args:
        name (str): Name of the memory
    Returns:
        str: Content of the memory
    """
    with open(f"./memory/{name}.md", "r") as f:
        return f.read()

def create_memory(name: str, content: str) -> str:
    """Create a new memory
    Args:
        name (str): Name of the memory
        content (str): Content of the memory
    Returns:
        str: Status message
    """
    with open(f"./memory/{name}.md", "w") as f:
        f.write(content)
    return f"Memory '{name}' created successfully"

def delete_memory(name: str) -> str:
    """Delete a memory
    Args:
        name (str): Name of the memory
    Returns:
        str: Status message
    """
    os.remove(f"./memory/{name}.md")
    return f"Memory '{name}' deleted successfully"
