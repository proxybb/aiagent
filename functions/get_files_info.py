import os

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

def get_files_info(working_directory: str, directory: str = ".") -> str:
    
    ## path validation
    
    try:
        working_dir_abs = os.path.abspath(working_directory)

        target_dir_abs = os.path.normpath(os.path.join(working_dir_abs, directory))

        # check if direct is valid (bool)
        is_valid_target_dir = os.path.commonpath([working_dir_abs, target_dir_abs]) == working_dir_abs

        if not is_valid_target_dir:
                return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir_abs):
                return f'Error: "{directory}" is not a directory'
        
    except Exception as e:
        return f"Error: {e}"


    try:
        items: list = []
        for item in os.listdir(target_dir_abs):
            path = os.path.normpath(os.path.join(target_dir_abs, item))
            items.append(f"  - {item}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)}")
        description: str = "\n".join(items)

    except Exception as e:
         return f"Error: {e}"

    if directory == ".":
        return f"Result for current directory:\n{description}"

    else:
        return f"Result for '{directory}' directory:\n{description}"