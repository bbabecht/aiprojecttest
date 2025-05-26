import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

# OpenAI LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini") # Default if not set

# Placeholder for other LLM related settings if needed
# Example: TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.7))

# For debugging purposes, you might want to print or log these
# Be careful not to log the API key in production environments
# print(f"OpenAI Model: {OPENAI_MODEL_NAME}")
# if not OPENAI_API_KEY:
#     print("Warning: OPENAI_API_KEY is not set.")
# else:
#     print(f"OpenAI API Key Loaded (first 5 chars): {OPENAI_API_KEY[:5]}...")

# This file will be imported by the agent to get these settings.
