import os
from enum import Enum
from utils import load_module, get_function_schema
from inspect import getmembers, isfunction
import json
import traceback

from openwebui_client import OpenWebUIClient

# Import configuration
from config import Config

# Validate configuration
try:
    Config.validate()
except ValueError as e:
    print(f"Configuration error: {e}")
    exit(1)

class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    FUNCTION = "function"

class Message:
    def __init__(self, role, content):
        self.role = role
        self.content = content

    def toJSON(self):
        return {
            "role": self.role.value,
            "content": self.content
        }

INSTRUCTION ='''\nYou are a helpful assistant. \n\nYour system consists of:\n- Interface (Text, Audio, Images): interface.py\n- Processing (Tools):   ./tools/{{tool_name}}.py\n- Memory (Context, Messages, Database): ./memory/{{memory_name}}.md\n\nYour actions are:\n- Read\n- Create/Update\n- Delete\n\nYou should improve yourself and the system. You can build tools, and memory.\nObserve your Processing files, tools and your Memory, context, messages, database and update them for improving:\n- Consistency\n- Completeness\n- Efficiency\n- Abstractions\n\nExample of a tool:\n\ndef tool_name(arg1: type1, arg2: type2) -> return_type:\n    """Description of the tool\n\n    Args:\n        arg1 (type1): description of arg1\n        arg2 (type2): description of arg2\n\n    Returns:\n        return_type: description of return_type\n    """\n'''

CONTEXT = Message(Role.SYSTEM, INSTRUCTION)
TOOLS_PATH = "./tools"

messages = [CONTEXT.toJSON()]

# Use configuration for model
MODEL = Config.DEFAULT_MODEL

import httpx
http_client = httpx.Client(verify=False)

# Initialize client with configuration
client = OpenWebUIClient(
    api_key=Config.KI_AWZ_API_KEY,
    base_url=Config.KI_AWZ_API_URL,
    default_model=MODEL,
    http_client=http_client
)

tools = []
available_functions = {}

tools_module = load_module(os.path.join(os.getcwd(), "tools", "system.py"))
available_functions_list = getmembers(tools_module, isfunction)

available_functions.update({k:v for k,v in available_functions_list})

for func_name, func in available_functions_list:
    if func.__module__ == tools_module.__name__:
        tools.append(get_function_schema(func))

print(tools)

while True:
    # Observe -> Context:
    # - Interface
    #       - Input
    #       - Output
    # - Processing
    #       - Consistency
    #       - Completeness
    #       - Efficiency
    # - Memory
    #       - Abstractions

    try:
        tools = []
        available_functions = {}

        for tool_path in os.listdir(TOOLS_PATH):
            if tool_path.endswith(".py") and tool_path != "__init__.py":
                tools_module = load_module(os.path.join(os.getcwd(), "tools", tool_path))
                available_functions_list = getmembers(tools_module, isfunction)

        available_functions.update({k:v for k,v in available_functions_list})

        for func_name, func in available_functions_list:
            if func.__module__ == tools_module.__name__:
                tools.append(get_function_schema(func))

        user_input = input("You: ")
        if user_input != "\n":
            messages.append(Message(Role.USER, user_input).toJSON())

        # response = client.chat_with_tools(messages=messages, tools=tools, tool_params=None, model=MODEL, max_tool_calls=None, files=None)
        # response = client.chat_with_tools(messages=messages, tools=tools, model=MODEL)

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )

        while (response.choices[0].message.tool_calls):
            # There may be multiple tool calls in the response
            for tool in response.choices[0].message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    answer = input("Calling function: " + tool.function.name + " with arguments: " + str(tool.function.arguments) + "\nAnswer: (y/n)")
                    # string to json
                    args = json.loads(tool.function.arguments)
                    if answer == "y":
                        output = function_to_call(**args)
                    else:
                        output = "User rejected function call"
                else:
                    output = "Function not found"

                # Only needed to chat with the model using the tool call results
                print(response.choices[0].message)
                messages.append(response.choices[0].message)
                print(output)
                messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})

                response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools) #, think=self.think)

        print(response.choices[0].message.content)
        messages.append(response.choices[0].message)

        # Plan -> Processing:
        # - Identify
        #       - Read
        # - Solve
        #       - Create/Update
        # - Evaluate
        
        # Act -> Interface:
        # - Update

    except Exception as e:
        tools = []
        available_functions = {}

        tools_module = load_module(os.path.join(os.getcwd(), "tools", "system.py"))
        available_functions_list = getmembers(tools_module, isfunction)

        available_functions.update({k:v for k,v in available_functions_list})

        for func_name, func in available_functions_list:
            if func.__module__ == tools_module.__name__:
                tools.append(get_function_schema(func))

        print(tools)

        print(traceback.format_exc())
        messages.append({'role': 'tool', 'content': str(traceback.format_exc()), 'tool_name': "error"})
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools) #, think=self.think)
        while (response.choices[0].message.tool_calls):
            # There may be multiple tool calls in the response
            for tool in response.choices[0].message.tool_calls:
                # Ensure the function is available, and then call it
                if function_to_call := available_functions.get(tool.function.name):
                    answer = input("Calling function: " + tool.function.name + " with arguments: " + str(tool.function.arguments) + "\nAnswer: (y/n)")
                    # string to json
                    args = json.loads(tool.function.arguments)
                    if answer == "y":
                        output = function_to_call(**args)
                    else:
                        output = "Function not called"
                else:
                    output = "Function not found"

                # Only needed to chat with the model using the tool call results
                print(response.choices[0].message)
                messages.append(response.choices[0].message)
                print(output)
                messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})

                response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools) #, think=self.think)

        print(response.choices[0].message.content)
        messages.append(response.choices[0].message)