import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import call_function

user_prompt = sys.argv[1]

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
messages = [ types.Content(role="user", parts=[types.Part(text=user_prompt)]), ]
arg = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read fuke contents
- Execute Python files with optional argumens
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

schema_get_files_info = types.FunctionDeclaration(
            name="get_files_info",
            description="List files in the specified directory along with their sizes, constrained to the working directory.",
            parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "directory": types.Schema(
                            type=types.Type.STRING,
                            description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                            )
                        },
                ),
        )
schema_get_file_content = types.FunctionDeclaration(
            name="get_file_content",
            description="Displays the content of a specified file.",
            parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="The path to the file which the content should be displayed",
                            )
                        },
                ),
        )
schema_run_python = types.FunctionDeclaration(
            name="run_python_file",
            description="Runs the specified python file.",
            parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="The path to the python file which should be executed.",
                            )
                        },
                ),
        )
schema_write_file = types.FunctionDeclaration(
            name="write_file",
            description="Writes content within a specified file..",
            parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "file_path": types.Schema(
                            type=types.Type.STRING,
                            description="The path to the file which the content should be written.",
                            ),
                        "content": types.Schema(
                            type=types.Type.STRING,
                            description="The content to be written in to the file instructed in the path."
                            )
                        },
                ),
        )

available_functions = types.Tool(
            function_declarations=[
                    schema_get_files_info,
                    schema_run_python,
                    schema_get_file_content,
                    schema_write_file,
                ]
        )

config = types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)

max_counter = 20
counter = 0
verbose = len(sys.argv) > 2 and sys.argv[2] == '--verbose'

while counter < 20:
    response = client.models.generate_content(
                    model="gemini-2.0-flash-001",
                    contents=messages,
                    config=config)
    if response.function_calls:
        for candidate in response.candidates:
            print(f"/n Candidate: {candidate}")
            messages.append(candidate.content)

        for function_call_part in response.function_calls:
            result = call_function(function_call_part, verbose)
            messages.append(result)
            part = result.parts[0]
            if hasattr(part, "function_response") and part.function_response:
                response = getattr(part.function_response, "response", None)
                if response is not None and verbose:
                    print(f"-> {result.parts[0].function_response.response['result']}")
                else:
                    raise RuntimeError("Something went fatally wrong.")
    else:
        print(f"{response.text}")
        break

    counter += 1




if len(sys.argv) > 2 and sys.argv[2] == '--verbose':
    print(f"User prompt: {user_prompt}")
   # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    #:print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
