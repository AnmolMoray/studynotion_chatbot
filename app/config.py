import os
from dotenv import load_dotenv
from groq import Groq, GroqError


# Load environment variables from .env file
load_dotenv()

# Retrieve the Groq API key from environment variables
api_key = os.environ.get("GROQ_API_KEY")

# Check if the API key was loaded successfully
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")

try:
    # Initialize Groq client with the retrieved API key
    client = Groq(api_key=api_key)

except GroqError as e:
    raise RuntimeError(f"Failed to initialize Groq client: {e}")

# Example usage (this part depends on what you want to do with the Groq client)
# response = client.some_function(...)  # Replace with actual function calls
