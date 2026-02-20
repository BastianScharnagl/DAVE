from fastapi import FastAPI
import json
import traceback
from enum import Enum
from inspect import getmembers, isfunction

import importlib.util
import sys
import string
import secrets
import inspect

import httpx
from dotenv import load_dotenv
import logging
from openwebui_client import OpenWebUIClient

import os
import argparse
import uvicorn

def gensym(length=32, prefix="gensym_"):
    """
    generates a fairly unique symbol, used to make a module name,
    used as a helper function for load_module

    :return: generated symbol
    """
    alphabet = string.ascii_uppercase + string.ascii_lowercase + string.digits
    symbol = "".join([secrets.choice(alphabet) for i in range(length)])

    return prefix + symbol


def load_module(source, module_name=None):
    """
    reads file source and loads it as a module

    :param source: file to load
    :param module_name: name of module to register in sys.modules
    :return: loaded module
    """

    if module_name is None:
        module_name = gensym()

    spec = importlib.util.spec_from_file_location(module_name, source)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    return module


def init(model: str = "lisa-v40-rc1-qwen3235b-a22b-instruct") -> tuple[OpenWebUIClient, list[dict]]:
    """Initialize the LLM client and register tools

    Returns:
        tuple: (client, messages)
    """

    load_dotenv()
    # ---------------------------------------------------------------------------
    # Initialization of LLM client 
    # https://github.com/bemade/openwebui-client
    # ---------------------------------------------------------------------------
    http_client = httpx.Client(verify=False)

    client = OpenWebUIClient(
        api_key=os.getenv("KI_AWZ_API_KEY"),
        base_url=os.getenv("KI_AWZ_API_URL"),
        default_model=model,
        http_client=http_client,
    )

    # ---------------------------------------------------------------------------
    # Initialization of system tools
    # ./actors/local/system.py
    # https://github.com/bemade/openwebui-client/blob/main/openwebui_client/tools.py
    # ---------------------------------------------------------------------------

    def register_tools(path: str) -> list[str]:
        """Register tools for the client to act with

        Args:
            path (str): The path to the directory containing the tools

        Returns:
            list: List of function names
        """
        tools_module = load_module(os.path.join(os.getcwd(), path))

        available_functions = getmembers(tools_module, isfunction)

        function_names = []
        for function in available_functions:
            client.tool_registry.register(function[1])
            function_names.append(function[0])
        
        return function_names

    client.tool_registry.register(register_tools)

    response = client.chat_with_tools(
        messages=[{"role": "system", "content": "Register your tools for acting in path actors/system.py"}],
        max_tool_calls=5
    )
    print(response)

    messages = []

    with open("main.md", "r") as f:
        system_message = {"role": "system", "content": f.read()}

    messages.append(system_message)

    """
    response = client.chat_with_tools(
        messages=messages,
        max_tool_calls=5
    )
    print(response)
    """
    return client, messages

parser = argparse.ArgumentParser()
parser.add_argument('--port', default=8000)
parser.add_argument('--model', default="lisa-v40-rc1-qwen3235b-a22b-instruct")
args = parser.parse_args()

client, messages = init(args.model)

# ---------------------------------------------------------------------------
# Initialization of API Route to interface with agent 
# https://fastapi.tiangolo.com/
# ---------------------------------------------------------------------------

app = FastAPI()

@app.post("/chat")
def chat(message: str):
    messages.append({
        "role": "user",
        "content": message
    })

    response = client.chat_with_tools(
        messages=messages,
        max_tool_calls=5
    )

    print("[MAIN]", response)

    return response

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=int(args.port))
