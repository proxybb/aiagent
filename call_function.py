import json
from collections.abc import Callable
from functions.get_files_info import *
from functions.get_file_content import *
from functions.write_files import *
from functions.run_python_file import *

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file
]

function_map: dict[str, Callable[..., str]] = {
    "get_file_content": get_file_content,
    "get_files_info": get_files_info,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

def call_function(tool_call, verbose: bool = False) -> dict:
    function_name = tool_call.function.name
    function_args: dict = json.loads(tool_call.function.arguments or "{}")
    function_args["working_directory"] = "./calculator"

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name in function_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": function_map[function_name](**function_args)
        }

    else:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }