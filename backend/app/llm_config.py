import os
from dotenv import load_dotenv

load_dotenv()

# Example:
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-3.5-turbo")

# Placeholder for now
LLM_PROVIDER = "None"
API_KEY = "dummy_api_key"
MODEL_NAME = "dummy_model"

print(f"LLM Provider: {LLM_PROVIDER}") # For debugging, can be removed later
print(f"Model Name: {MODEL_NAME}") # For debugging, can be removed later
