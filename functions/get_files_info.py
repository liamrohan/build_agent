import textwrap
from os import listdir, path

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}


def get_files_info(working_dir: str, directory: str = ".") -> str:
    try:
        working_dir_abs = path.abspath(path=working_dir)
        target_dir = path.normpath(path.join(working_dir_abs, directory))
        valid_target_dir = (
            path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory, or it\'s not here'

        file_strings: list[str] = []
        target_dir_contents = listdir(target_dir)
        for item in target_dir_contents:
            try:
                is_dir = path.isdir(path.join(target_dir, item))
                file_name = item
                file_size = path.getsize(path.join(target_dir, file_name))
                file_str = (
                    f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"
                )
                file_strings.append(file_str)

            except Exception as e:
                return f"Error: something went wrong"

        curr_dir_str: str = (
            "current directory"
            if directory == "." or directory == "./"
            else f"'{directory}'"
        )
        file_info_final_str = textwrap.dedent(
            f"Result for {curr_dir_str}:\n"  # pyright: ignore[reportImplicitStringConcatenation]
            f"  {'  '.join(file_strings)}"
        )
        print(file_info_final_str)

    except Exception as e:
        return f'Error: failed for some reason with - "{e}"'

    return file_info_final_str
