import os

def write_file(working_directory, file_path, content):
    working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.join(working_path, file_path)
    if not abs_file_path.startswith(working_path):
        return f"Error: Cannot write to {file_path} as it is outside the permitted working directory"

    file_dir_path = abs_file_path.replace(file_path, '')
    if not os.path.exists(file_dir_path):
        os.makedirs(file_dir_path)

    with open(abs_file_path, "w") as f:
        f.write(content)

    return f"Successfully wrote to {file_path} ({len(content)} characters written)"
