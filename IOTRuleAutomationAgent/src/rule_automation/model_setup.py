import os

from langchain_groq import ChatGroq
from dotenv import load_dotenv


def get_llm():
    load_dotenv()
    groq_api_key = os.getenv("GROQ_API_KEY")

    if not groq_api_key:
        raise ValueError("GROQ_API_KEY is not set. Add it to your .env file.")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        groq_api_key=groq_api_key,
        temperature=0,
    )

    return llm
