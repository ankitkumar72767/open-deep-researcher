# config.py
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not set")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not set")
