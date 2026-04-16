import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

client = Groq(api_key=groq_api_key)

models = client.models.list()

print("Available Models:\n")
for model in models.data:
    print("-", model.id)
