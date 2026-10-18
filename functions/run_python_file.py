import subprocess
import textwrap
import time
from os import path

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Given a python file, it attempts to run it, providing output on STDOUT, STDERR, etc",
        "parameters": {
            "type": "object",
            "required": ["args", "file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The proposed python file that should be run. It has to be a python file for this to work",
                },
                "args": {
                    "type": "array",
                    "description": "A list of arguments passed appended to the pythong command",
                    "items": {"type": "string", "description": "A command argument"},
                },
            },
        },
    },
}


def run_python_file(
    working_dir: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = path.abspath(working_dir)
        target_file = path.normpath(path.join(working_dir_abs, file_path))
        is_inside_working_dir = (
            path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        is_file = path.isfile(target_file)

        if not is_inside_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not is_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not str.endswith(target_file, ".py"):
            return f'Error: "{file_path}" is not a Python file'

    except Exception as e:
        return f"Error: issue verifying paths"

    command = ["python", target_file]
    if args and len(args) > 0:
        for arg in args:
            command.extend(arg)

    try:
        output = subprocess.run(command, capture_output=True, text=True)
        time.sleep(4)
        return_code = output.returncode
        if return_code > 0:
            return f"Process existed with code {return_code}"
        no_output = output.stderr and output.stdout == ""
        if no_output:
            return f"No output produced"
        return textwrap.dedent(f"""
        STDOUT: {output.stdout}
        STDERR: {output.stderr}
        """)

    except Exception as e:
        return f"Error: executing Python file: {e}"
