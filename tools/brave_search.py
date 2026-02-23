import os
import requests
from typing import Dict, Any

def brave_search(query: str, count: int = 10, offset: int = 0) -> Dict[str, Any]:
    """
    Perform a web search using the Brave Search API.
    
    Args:
        query (str): The search query
        count (int): Number of results to return (default: 10)
        offset (int): Offset for pagination (default: 0)
    
    Returns:
        Dict[str, Any]: Search results from Brave Search API
    """
    # Read API key from .env file
    with open('.env', 'r') as file:
        for line in file:
            if line.startswith('BRAVE_SEARCH_API_KEY'):
                api_key = line.split('=')[1].strip()
                break
    
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        'Accept': 'application/json',
        'X-Subscription-Token': api_key
    }
    params = {
        'q': query,
        'count': count,
        'offset': offset
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    return {"error": "Unknown error occurred"}