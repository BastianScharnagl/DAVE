from openwebui_client import OpenWebUIClient
import os
import json
import traceback
from enum import Enum
from utils import load_module, get_function_schema
from inspect import getmembers, isfunction

import httpx
from dotenv import load_dotenv

#import logging
#logging.basicConfig(filename="main.log", level=logging.DEBUG)

MODEL="lisa-v40-rc1-qwen3235b-a22b-instruct"

load_dotenv()

# ---------------------------------------------------------------------------
# Initialization of LLM client 
# https://github.com/bemade/openwebui-client
# ---------------------------------------------------------------------------
http_client = httpx.Client(verify=False)

client = OpenWebUIClient(
    api_key=os.getenv("KI_AWZ_API_KEY"),
    base_url=os.getenv("KI_AWZ_API_URL"),
    default_model=MODEL,
    http_client=http_client,
)

# ---------------------------------------------------------------------------
# Initialization of system tools
# ./tools/system.py
# https://github.com/bemade/openwebui-client/blob/main/openwebui_client/tools.py
# ---------------------------------------------------------------------------
def register_tools(path: str) -> list[str]:
    """Register tools for the client to act with

    Args:
        path (str): The path to the directory containing the tools

    Returns:
        list: List of function names
    """
    print(path)
    tools_module = load_module(os.path.join(os.getcwd(), path))

    available_functions = getmembers(tools_module, isfunction)

    function_names = []
    for function in available_functions:
        client.tool_registry.register(function[1])
        function_names.append(function[0])
    
    return function_names


client.tool_registry.register(register_tools)

response = client.chat_with_tools(
    messages=[{"role": "system", "content": "Register your tools for acting in path tools/system.py"}],
    max_tool_calls=5
)
print(response)

messages = []

with open("main.md", "r") as f:
    system_message = {"role": "system", "content": f.read()}

messages.append(system_message)

with open("README.md", "r") as f:
    system_message = {"role": "system", "content": f.read()}

messages.append(system_message)

"""
response = client.chat_with_tools(
    messages=messages,
    max_tool_calls=5
)
print(response)
"""


"""
system_message = {"role": "system", "content": "Run the internet server with command python sensors/server.py --port 8000 --model lisa-code-101 in background to have a programmer working for you"}

messages.append(system_message)

response = client.chat_with_tools(
    messages=messages,
    max_tool_calls=10
)
print(response)
"""

# ---------------------------------------------------------------------------
# Main agent loop
# ---------------------------------------------------------------------------
while True:
    # SENSE
    # Observe yourself and your environment

    # THINK
    # Plan your actions

    # ACT
    # Create and register new tools. Explore APIs. Refactor and restructurize your code.

    try:       
        # --- User input ---
        user_input = input("Your message: ")
        if user_input != "\n":
            messages.append({
                "role": "user",
                "content": user_input
            })

        response = client.chat_with_tools(
            messages=messages,
            max_tool_calls=100
        )

        print("[MAIN]", response)
        messages.append({"role": "assistant", "content": response})

    except Exception:
        exception_string = traceback.format_exc()
        print("[ERROR]", exception_string)
        messages.append({"role": "system", "content": exception_string})
