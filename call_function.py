from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import schema_write_file

available_functions = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_file_content, schema_run_python_file, schema_write_file],
)