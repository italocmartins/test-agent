import os

def get_files_info(working_directory, directory=None):
    if directory == None:
        return "Give a valid directory"

    working_path = os.path.abspath(working_directory)
    directory_path = os.path.join(working_path, directory)
    if not directory_path.startswith(working_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(directory_path):
        return f'Error: "{directory}" is not a directory'

    files = os.listdir(directory_path)
    for i in range(0, len(files)):
        file_path = f"{directory_path}/{files[i]}"
        file_size = os.path.getsize(file_path)
        is_dir = os.path.isdir(file_path)
        print(f'{files[i]}: file_size={file_size} bytes, is_dir={is_dir}')

