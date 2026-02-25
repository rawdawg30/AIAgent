import os, argparse
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Api key not found")

from google import genai
from prompts import system_prompt
from call_function import available_functions

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
    response = client.models.generate_content(model='gemini-2.5-flash', 
                                              contents=messages, 
                                              config=types.GenerateContentConfig(
                                                  tools=[available_functions],
                                                  system_instruction=system_prompt,
                                                  temperature=0)) #"Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")
    
    if response.usage_metadata == None:
        raise RuntimeError("Failed API request: None response")
    
    if (args.verbose):
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.function_calls == None:
        print(response.text)
    else:
        for item in response.function_calls:
            print(f"Calling function: {item.name}({item.args})")

if __name__ == "__main__":
    main()
