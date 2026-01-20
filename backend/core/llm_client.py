import os
import json
from typing import Type, TypeVar, Optional
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# Try to find .env file
dotenv_path = find_dotenv(usecwd=True)
if not dotenv_path:
    # Fallback: looks like we are in backend/core, try 2 levels up
    potential_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env")
    if os.path.exists(potential_path):
        dotenv_path = potential_path

print(f"DEBUG: Loading .env from: {dotenv_path}")
load_dotenv(dotenv_path)

T = TypeVar('T', bound=BaseModel)

# Mock OpenAI client if key is missing (for safety/testing without key)
class MockOpenAI:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def chat(self, *args, **kwargs):
        raise ValueError("OpenAI API Key not found. Please set OPENAI_API_KEY in .env")

# Initialize Client
api_key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: API Key loaded: {'Yes' if api_key else 'No'} (starts with {api_key[:5] if api_key else 'None'})")

is_groq = api_key and api_key.startswith("gsk_")

try:
    if is_groq:
        print("DEBUG: Detected Groq API Key. Using Groq base_url.")
        client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
    elif api_key:
         client = OpenAI(api_key=api_key)
    else:
         client = None # Handle gracefully in calls
except Exception as e:
    print(f"Warning: OpenAI client failed to init: {e}")
    client = None

def get_llm_response(
    system_prompt: str,
    user_prompt: str,
    response_model: Type[T],
    model: str = "llama-3.3-70b-versatile" if is_groq else "gpt-4o-mini"
) -> T:
    """
    Generic wrapper for structured LLM calls.
    Enforces JSON mode and Pydantic validation.
    """
    if not client:
        # Return a dummy response for testing if no client (OR RAISE ERROR)
        # For production readiness, we should probably raise an error
        raise ValueError("OpenAI API Key is missing. Please set OPENAI_API_KEY environment variable.")

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.0  # Deterministic
        )
        
        content = completion.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")
            
        data = json.loads(content)
        return response_model(**data)
        
    except Exception as e:
        print(f"LLM Call Error: {e}")
        raise e
