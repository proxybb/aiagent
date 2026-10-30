import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "writes to a specified file in a specified directory relative to the working directory with the provided content",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                     "type": "string",
                     "description": "File path to the file we are writing to, relative to the working directory"
                },
                "content": {
                     "type": "string",
                     "description": "Content to be written to the specified file"     
                }
            },
        },
    },
}

def write_file(working_directory: str, file_path: str, content: str) -> str:
    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # check if direct is valid (bool)
        is_valid_file = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs

        if not is_valid_file:
                return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_file_path):
                return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
        
    except Exception as e:
        return f"Error: {e}"

    try:
          with open(abs_file_path, "w") as f:
                f.write(content)

    except Exception as e:
        return f"Error: {e}"
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'