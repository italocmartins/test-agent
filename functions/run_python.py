import os
import subprocess

def run_python_file(working_directory, file_path):
    working_path = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_path, file_path))
    if not abs_file_path.startswith(working_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if ".py" not in file_path:
        return f"Error: {file_path} is not a Python file."

    try:
        result = subprocess.run(["python", abs_file_path], timeout=30, capture_output=True, text=True)
   
        result.check_returncode()

        if result.stdout.strip() == "" and result.stderr.strip() == "":
            return "No output produced."
        
        return f"Successfully runned {file_path}, STDOUT: {result.stdout} , STDERR: {result.stderr}"

    except subprocess.TimeoutExpired as e:
        return f"Timout error {e}"
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {result.returncode}"	

    return f"Successfully runned {file_path}, STDOUT: {result.stdout} , STDERR: {result.stderr}"
