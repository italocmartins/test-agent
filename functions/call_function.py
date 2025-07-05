from .run_python import run_python_file
from .get_file_content import get_file_content
from .get_files_info import get_files_info
from .write_file import write_file
from google.genai import types

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f" - Calling function: {function_call_part.name}({function_call_part.args})")
    else: 
        print(f" - Calling function: {function_call_part.name}")
    function_registry = { "run_python_file": run_python_file, "get_file_content": get_file_content, "get_files_info": get_files_info, "write_file": write_file }

    if function_call_part.name in function_registry:
        result = function_registry[function_call_part.name]( './calculator',**function_call_part.args)
        return types.Content(
                    role="tool",
                    parts=[
                        types.Part.from_function_response(
                                name=function_call_part.name,
                                response={"result": result}
                            )
                        ]
                )
    else:
        return types.Content(
                    role="tool",
                    parts=[
                            types.Part.from_function_response(
                                    name=function_call_part.name,
                                    response={"error": f"Unkown function: {function_call_part.name }"}
                                )
                        ]
                )




