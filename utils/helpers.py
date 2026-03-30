from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq
from pathlib import Path

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

def get_llm():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not found! Make sure .env exists with GROQ_API_KEY=your_key"
        )
    return ChatGroq(
        model="llama-3.3-70b-versatile",  # 70B — required for multi-tool reasoning
        temperature=0.5,                   # slightly lower = more consistent outputs
        max_tokens=2048,                   # cap output length = faster responses
        api_key=api_key
    )