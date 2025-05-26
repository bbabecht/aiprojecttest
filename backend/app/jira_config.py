import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

JIRA_API_KEY = os.getenv("JIRA_API_KEY")
JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")

# For debugging purposes
# if not JIRA_API_KEY:
#     print("Warning: JIRA_API_KEY is not set.")
# else:
#     print(f"Jira API Key Loaded (first 5 chars): {JIRA_API_KEY[:5]}...")
# if not JIRA_BASE_URL:
#     print("Warning: JIRA_BASE_URL is not set.")
# else:
#     print(f"Jira Base URL: {JIRA_BASE_URL}")
