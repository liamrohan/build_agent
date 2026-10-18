from os import makedirs, path

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes to a specified file path relative to the working directory, providing information of success or failure. This operation overwrites existing files or creates new ones.",
        "parameters": {
            "type": "object",
            "required": ["file_path", "content"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The proposed file that should be written to",
                },
                "content": {
                    "type": "string",
                    "description": "The content that should be written to the file",
                },
            },
        },
    },
}


def write_file(working_dir: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = path.abspath(path=working_dir)
        target_file = path.normpath(path.join(working_dir_abs, file_path))
        is_inside_working_dir = (
            path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        is_dir = path.isdir(target_file)

        if not is_inside_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if is_dir:
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        is_file_exists = path.isfile(target_file)
        if not is_file_exists:
            makedirs(name=working_dir_abs, exist_ok=True)

        try:
            with open(file=target_file, mode="w", encoding="utf-8") as f:
                _ = f.write(content)
        except Exception as e:
            return f"Error: couldn't write: {e}"

    except Exception as e:
        return f"Error: Something bad happened: {e}"
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
