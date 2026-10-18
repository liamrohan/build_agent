from os import path

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Returns the first 10000 characters within a provided file path if it exists, or provides a string error if the read operation failed",
        "parameters": {
            "type": "object",
            "required": ["file_path"],
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The proposed file that should be read from",
                }
            },
        },
    },
}


def get_file_content(working_dir: str, file_path: str) -> str:
    MAX_CHARS = 10000
    try:
        working_dir_abs = path.abspath(path=working_dir)
        target_file = path.normpath(path.join(working_dir_abs, file_path))
        valid_target_file = (
            path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        content_of_file = ""

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        try:
            with open(target_file, mode="r", encoding="utf-8") as file:
                f = file.read(MAX_CHARS)
                content_of_file += f
                if file.read(1):
                    content_of_file += (
                        f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                    )
        except Exception as e:
            return f"Error: something went wrong reading the file"

    except Exception as e:
        return f'Error: failed for some reason with - "{e}"'

    return content_of_file
