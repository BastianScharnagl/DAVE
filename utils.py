import importlib.util
import sys
import string
import secrets
import inspect


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


def get_type_name(t):
    if t == inspect.Parameter.empty:
        return "string"
    if t is str:
        return "string"
    if t is int:
        return "integer"
    if t is float:
        return "number"
    if t is bool:
        return "boolean"
    if t is dict:
        return "object"
    if t is list:
        return "array"
    return "string"


def get_function_schema(func):
    sig = inspect.signature(func)
    doc = inspect.getdoc(func)
    
    description = ""
    param_descriptions = {}
    
    if doc:
        # Split docstring into description and params
        lines = doc.split("\n")
        desc_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith(":param"):
                # Parse param description
                # :param name: description
                parts = line.split(":", 2)
                if len(parts) >= 3:
                    param_name = parts[1].replace("param", "").strip()
                    param_desc = parts[2].strip()
                    param_descriptions[param_name] = param_desc
            elif line.startswith(":return"):
                continue
            else:
                if line:
                    desc_lines.append(line)
        description = " ".join(desc_lines).strip()
    
    parameters = {
        "type": "object",
        "properties": {},
        "required": []
    }
    
    for name, param in sig.parameters.items():
        param_type = get_type_name(param.annotation)
        
        parameters["properties"][name] = {
            "type": param_type,
            "description": param_descriptions.get(name, "")
        }
        
        if param.default == inspect.Parameter.empty:
            parameters["required"].append(name)
            
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": description,
            "parameters": parameters
        }
    }