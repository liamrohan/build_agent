import json
from collections.abc import Callable
from typing import Any

from openai.types.chat import (
    ChatCompletionMessageToolCall,
    ChatCompletionMessageToolCallUnion,
    ChatCompletionToolMessageParam,
)

from functions.get_file_content import get_file_content, schema_get_file_content
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import schema_write_file, write_file

avaialble_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file,
]


def call_function(
    tool_call: ChatCompletionMessageToolCallUnion, verbose: bool = False
) -> ChatCompletionToolMessageParam:
    fn_id = tool_call.id
    fn_name = ""
    fn_args: dict[str, Any] = {}

    if isinstance(tool_call, ChatCompletionMessageToolCall):
        fn_name = tool_call.function.name
        fn_args = json.loads(tool_call.function.arguments)

    if verbose:
        print(f"\n - Calling function: {fn_name}({fn_args})\n")
    else:
        print(f"\n - Calling function: {fn_name}\n")

    func_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if not func_map[fn_name]:
        print("ERRORS: func_map")
        return {
            "role": "tool",
            "tool_call_id": fn_id,
            "content": f"Error: Unknown function: {fn_name}",
        }

    fn_args["working_dir"] = "./calculator"
    r = func_map[fn_name](**fn_args)
    tool_resp:ChatCompletionToolMessageParam = {"role": "tool", "tool_call_id": fn_id, "content": r}
    return tool_resp
