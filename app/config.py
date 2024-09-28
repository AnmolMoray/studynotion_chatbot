import os
from dotenv import load_dotenv
from groq import Groq
import openai

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)