# config/settings.py

from dotenv import load_dotenv
import os

load_dotenv()

# Default models by provider
DEFAULT_MODELS = {
    "openai": "gpt-5-pro-2025-10-06",
    "anthropic": "claude-sonnet-4-5",
    "google": "gemini-2.5-pro",
}

API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY"),
    "anthropic": os.getenv("ANTHROPIC_API_KEY"),
    "google": os.getenv("GOOGLE_API_KEY"),
}