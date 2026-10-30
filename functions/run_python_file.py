import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a specified file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                     "type": "string",
                     "description": "File path to run the file, relative to the working directory"
                },
                "args": {
                     "type": "array",
                     "items": {"type": "string"},
                     "description": "Optional arguements to run the executable"     
                }
            },
        },
    },
}

def run_python_file(
        working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        working_dir_abs = os.path.abspath(working_directory)

        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # check if direct is valid (bool)
        is_valid_file = os.path.commonpath([working_dir_abs, abs_file_path]) == working_dir_abs

        if not is_valid_file:
                return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
                return f'Error: "{file_path}" does not exist or is not a regular file'

        if not abs_file_path.endswith('.py'):
              return f'Error: "{file_path}" is not a Python file'
        
    except Exception as e:
        return f"Error: {e}"

    
    try:
        command = ["python", abs_file_path]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, timeout=30)

        description: list[str] = []
        
        if result.returncode != 0:
            description.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            description.append("No output produced")

        if result.stdout:
            description.append(f"STDOUT: {result.stdout}")

        if result.stderr:
            description.append(f"STDERR: {result.stderr}")

        status = "\n".join(description)

        return status

    except Exception as e:
            return f"Error: {e}"