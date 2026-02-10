import os
def get_files_info(working_directory, directory="."):
    try:
        abs_path = os.path.abspath(working_directory)
        full_path = os.path.normpath(os.path.join(abs_path, directory))
        valid_target_dir = os.path.commonpath([abs_path, full_path]) == abs_path
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # directory error return f'Error: "{directory}" is not a directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory' 

        contents = os.listdir(full_path)
        dir_contents = []
        dir_str = ""
        for item in contents:
            path = os.path.join(full_path, item)
            dir_contents.append(f"- {item}: file_size={os.path.getsize(path)}, is_dir={os.path.isdir(path)}")
                        
        return '\n'.join(dir_contents)

        return dir_str
    except Exception as e:
        return f'Error listing files: {e}'