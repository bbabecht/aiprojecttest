import requests
from .. import jira_config # To get JIRA_API_KEY and JIRA_BASE_URL
import json # For parsing JSON response

def get_jira_issue(issue_id_or_key: str) -> str:
    """
    Fetches details for a specific Jira issue using its ID or key.

    Args:
        issue_id_or_key: The ID or key of the Jira issue (e.g., "PROJECT-123").

    Returns:
        A string containing the JSON response from the Jira API for the issue,
        or an error message if the request fails.
    """
    if not jira_config.JIRA_API_KEY or not jira_config.JIRA_BASE_URL:
        return "Error: Jira API Key or Base URL is not configured."

    # Ensure the base URL doesn't have a trailing slash, then append the API path
    base_url = jira_config.JIRA_BASE_URL.rstrip('/')
    url = f"{base_url}/rest/api/3/issue/{issue_id_or_key}"

    headers = {
        "Authorization": f"Bearer {jira_config.JIRA_API_KEY}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10) # 10 seconds timeout
        response.raise_for_status() # Raises an HTTPError for bad responses (4XX or 5XX)
        
        # We can return the full JSON, or extract specific fields.
        # For now, returning the summary, status, and assignee for brevity.
        # If the LLM needs more, we can adjust this or return response.text / response.json()
        issue_data = response.json()
        summary = issue_data.get("fields", {}).get("summary", "N/A")
        status = issue_data.get("fields", {}).get("status", {}).get("name", "N/A")
        assignee = issue_data.get("fields", {}).get("assignee")
        assignee_name = assignee.get("displayName", "Unassigned") if assignee else "Unassigned"
        
        return json.dumps({
            "key": issue_data.get("key"),
            "summary": summary,
            "status": status,
            "assignee": assignee_name,
            "url": f"{base_url}/browse/{issue_data.get('key')}"
        })

    except requests.exceptions.HTTPError as http_err:
        # Attempt to get more specific error from Jira response
        try:
            error_json = response.json()
            messages = error_json.get("errorMessages", [])
            errors = error_json.get("errors", {})
            if messages:
                return f"Error fetching Jira issue {issue_id_or_key}: {response.status_code} {response.reason}. Jira messages: {'; '.join(messages)}"
            if errors:
                return f"Error fetching Jira issue {issue_id_or_key}: {response.status_code} {response.reason}. Jira errors: {json.dumps(errors)}"
        except ValueError: # If response is not JSON
            pass # Fall through to generic error
        return f"Error fetching Jira issue {issue_id_or_key}: {http_err}"
    except requests.exceptions.RequestException as req_err:
        return f"Error fetching Jira issue {issue_id_or_key}: {req_err}"
    except Exception as e:
        return f"An unexpected error occurred while fetching Jira issue {issue_id_or_key}: {e}"

# Example usage (for testing locally, not part of the tool itself for the agent)
# if __name__ == '__main__':
#     # Make sure to have a .env file in the backend directory with your credentials
#     # and run this script from the backend directory: python -m app.tools.jira_tool
#     print("Attempting to fetch JIRA issue (ensure .env is set up)...")
#     # Replace 'YOUR-ISSUE-KEY' with a real issue key from your Jira instance
#     test_issue_key = os.getenv("JIRA_TEST_ISSUE_KEY", "PROJECT-1") 
#     result = get_jira_issue(test_issue_key)
#     print(result)
