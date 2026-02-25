import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(full_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w') as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    
    except Exception as e:
        return f"Error: {e}"

     
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites or creates file at file specified",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of file to get write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="This string is what will be written into the specified file"
            )
        },
        required=["file_path", "content"]
    ),
)