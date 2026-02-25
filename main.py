import os
import json
import traceback
from utils import load_module
from inspect import getmembers, isfunction
from datetime import datetime
import httpx
from dotenv import load_dotenv
from openwebui_client import OpenWebUIClient

from tools.system import read_directory

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
    """Register tools for the agent/yourself to act with

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

# ---------------------------------------------------------------------------
# Poll signal messages in ./interfaces/signals
# ---------------------------------------------------------------------------
def poll_signals():
    signals = read_directory(os.path.join("interfaces", "signals"))

    if len(signals) > 0:
        signal = signals[-1]

        with open(os.path.join("interfaces", "signals", signal), "r") as f:
            message = f.readlines()

        os.remove(os.path.join("interfaces", "signals", signal))

        return message

    return None

# ---------------------------------------------------------------------------
# Reflect over your current knowledge and improve your knowledge graph
# ---------------------------------------------------------------------------
def reflect(input, output, n):
    # read files
    # compress files
    # save abstraction
    # improve knowledge graph
    await cognee.add(os.path.abspath("data/copilot_conversations.json"), node_set=["developer_data"])

client.tool_registry.register(register_tools)

tools = read_directory("tools")
for tool in tools:
    register_tools(tool)

messages = []

with open("main.md", "r") as f:
    system_message = {"role": "system", "content": f.read()}

messages.append(system_message)

with open("README.md", "r") as f:
    system_message = {"role": "system", "content": f.read()}

messages.append(system_message)
messages.append({"role": "system", "content": "improve yourself by writing your code. check your codebase and database and implement abstractions. Create new tools and use existing APIs. You can search the internet for public APIs."})

# ---------------------------------------------------------------------------
# Main agent loop
# ---------------------------------------------------------------------------
while True:
    try:
        # SENSE - Poll signals. Observe your codebase, database and your environment.
        signal = poll_signals()
        if signal:
            print("[SIGNAL]", signal)
            messages.append({
                "role": "user",
                "content": signal
            })
        else:
            signal = input("Your message: ")
            if signal == "\n":
                signal = None

        # THINK - Plan your actions
        tools = client.tool_registry.get_openai_tools()

        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)

        # ACT - Create and register new tools. Explore APIs. Refactor and restructurize your code base.
        #while (response.choices[0].message.tool_calls):
        for tool_call in response.choices[0].message.tool_calls:
            result = client.tool_registry.call_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            print("[TOOL]", tool_call.function.name, tool_call.function.arguments, result)
            messages.append({"role":"tool", "tool_call_id": tool_call.id, "content": str(result)})
    
            # MEMORIZE - Store the signal and the results of the consequential actions.
            """
            with open(os.path.join("memory", signal + "_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".json"), "w") as f:
                data = {
                    "signal": signal,
                    "tool": tool_call.function.name,
                    "args": tool_call.function.arguments,
                    "result": result 
                }
                json.dump(data, f)
            """

        print("[MAIN]", response.choices[0].message.content)


    except Exception:
        exception_string = traceback.format_exc()
        print("[ERROR]", exception_string)
        messages.append({"role": "system", "content": exception_string})
