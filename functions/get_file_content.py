import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads files in a specified directory relative to the working directory, providing its content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                     "type": "string",
                     "description": "File path to list content from, relative to the working directory"
                }
            },
        },
    },
}

MAX_CHARS = 100000

def get_file_content(working_directory: str, file_path: str) -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # check if direct is valid (bool)
        is_valid_file = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs

        if not is_valid_file:
                return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
                return f'Error: File not found or is not a regular file: "{file_path}"'
        
    except Exception as e:
        return f"Error: {e}"

    try:
        with open(abs_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                    file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
    except Exception as e:
        return f"Error: {e}"

    return file_content
    