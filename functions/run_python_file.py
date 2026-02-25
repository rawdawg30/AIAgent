import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not full_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", full_path]
        if args:
            command.extend(args)
        
        output = subprocess.run(command, cwd=abs_path, capture_output=True, text=True, timeout=30)

        outputstring = ""
        if not output.returncode == 0:
            outputstring = outputstring + f"Process exited with code {output.returncode}"
        if not output.stdout and not output.stderr:
            outputstring = outputstring + "No output produced"
        if output.stdout:
            outputstring = outputstring + f"STDOUT: {output.stdout}"
        if output.stderr:
            outputstring = outputstring + f"STDERR: {output.stderr}"
        
        return outputstring
    except Exception as e:
        return f"Error: executing Python file: {e}"

  
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs specified python file and returns the output of the execution as a string",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of python file relative to working directory that is to be executed",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="A list of things"
            )
        },
        required=["file_path"]
    ),
)