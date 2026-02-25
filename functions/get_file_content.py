import os
from google.genai import types
#import sys
#sys.path.append('../')

#from AIAGENT import MAX_CHARS
def get_file_content(working_directory, file_path):
    try:
        # return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        # if file path is outside working directory
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, file_path))
        valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
        if not valid_target_dir:
                return f'Error: Cannot list "{file_path}" as it is outside the permitted working directory'

        #if file not a file
        #return(f'Error: File not found or is not a regular file: "{file_path}"')
        if not (os.path.isfile(full_path)):
            return f'Error: File nor found or is not a regular file: "{file_path}"'
        #read file and return as string
        # use .read() with 10000 as limit on chars
        return_str = ""
        with open(full_path) as f:  
            return_str =  f.read(10000)
            if f.read(1):
                return_str += f'[...File "{file_path}" truncated at 10000 characters]'
            
        return return_str
    
    except Exception as e:
         return f"Error: {e}"
        
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Returns a string containing the contents of the file specified",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Name of file to get content from, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)