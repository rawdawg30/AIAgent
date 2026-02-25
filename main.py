import os, argparse
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Api key not found")

from google import genai
from prompts import system_prompt
from call_function import *

client = genai.Client(api_key=api_key)

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    for _ in range(20):
        response = client.models.generate_content(model='gemini-2.5-flash', 
                                                contents=messages, 
                                                config=types.GenerateContentConfig(
                                                    tools=[available_functions],
                                                    system_instruction=system_prompt,
                                                    temperature=0)) #"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
        if response.candidates:
            for item in response.candidates:
                messages.append(item)
        if response.usage_metadata == None:
            raise RuntimeError("Failed API request: None response")
        
        if (args.verbose):
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        function_results = []
        if response.function_calls == None:
            print(response.text)
            break
        else:
            for item in response.function_calls:
                call_function_result = call_function(item, args.verbose)
                if call_function_result.parts == []:
                    raise Exception
                if call_function_result.parts[0].function_response == None:
                    raise Exception
                if call_function_result.parts[0].function_response.response == None:
                    raise Exception
                function_results.append(call_function_result.parts[0])
                
                if args.verbose == True:
                    print(f"-> {call_function_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))
    print("Max aiagent iterations reached.")
if __name__ == "__main__":
    main()
