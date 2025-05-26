from fastapi.testclient import TestClient
from ..app.main import app # Adjusted import path
from unittest.mock import patch, MagicMock # For mocking
import os
import pytest # For environment variable setting in tests
from langchain_core.messages import AIMessage # Added import
import json # Added import

client = TestClient(app)

# Set dummy environment variables for testing if not already set
# This is crucial because llm_config and jira_config will try to load them
# In a real CI environment, these might be set externally.
@pytest.fixture(autouse=True)
def set_env_vars(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test_openai_key")
    monkeypatch.setenv("OPENAI_MODEL_NAME", "test_model")
    monkeypatch.setenv("JIRA_API_KEY", "test_jira_key")
    monkeypatch.setenv("JIRA_BASE_URL", "https://testjira.example.com")

# Mock the ChatOpenAI class to prevent actual API calls during tests
@pytest.fixture(autouse=True)
def mock_openai():
    with patch('backend.app.agent.ChatOpenAI') as mock_chat_openai:
        mock_llm_instance = MagicMock()
        # Configure the mock_llm_instance.invoke().content
        # For simplicity, let's make it echo the input or return a fixed message
        # More complex mocking can simulate tool calls.
        
        # This mock will be used by call_model_node
        # We need to mock the .bind_tools().invoke() chain.
        mock_bound_llm = MagicMock()
        
        # Default behavior: simple echo for non-tool-related prompts
        default_ai_response = AIMessage(content="LLM mock response to prompt.")
        mock_bound_llm.invoke.return_value = default_ai_response
        
        mock_llm_instance.bind_tools.return_value = mock_bound_llm
        mock_chat_openai.return_value = mock_llm_instance
        yield mock_chat_openai, mock_bound_llm # yield the mock for specific test adjustments


def test_handle_prompt_general_query(mock_openai):
    # Test with a general prompt that shouldn't trigger the Jira tool
    # The mocked LLM will return a generic response
    _, mock_bound_llm = mock_openai # Get the mock_bound_llm to set specific return values if needed
    mock_bound_llm.invoke.return_value = AIMessage(content="Hello from mock LLM!")

    response = client.post("/api/prompt", json={"prompt": "Hello there"})
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Hello from mock LLM!"
    assert data["error"] is None

def test_handle_prompt_empty_prompt(mock_openai):
    _, mock_bound_llm = mock_openai
    mock_bound_llm.invoke.return_value = AIMessage(content="Mock response to empty prompt.")

    response = client.post("/api/prompt", json={"prompt": ""})
    assert response.status_code == 200
    data = response.json()
    assert data["response"] == "Mock response to empty prompt."
    assert data["error"] is None

# This is the new test for the Jira tool, using mocking
def test_handle_prompt_with_jira_tool_mocked(mock_openai):
    # We need to make the mocked LLM "request" the Jira tool,
    # and then provide a "response" as if the tool executed.

    _, mock_bound_llm = mock_openai

    # Simulate LLM deciding to call the Jira tool
    jira_tool_call_id = "tool_call_jira_123"
    llm_response_requesting_tool = AIMessage(
        content="Okay, I will fetch that Jira issue.",
        tool_calls=[{
            "id": jira_tool_call_id,
            "name": "get_jira_issue_details",
            "args": {"issue_id_or_key": "TEST-123"}
        }]
    )
    
    # Simulate LLM processing the tool's output and giving a final answer
    final_llm_response_after_tool = AIMessage(
        content="Jira issue TEST-123 summary is 'Mocked Summary'."
    )

    # Set up the sequence of LLM responses
    mock_bound_llm.invoke.side_effect = [
        llm_response_requesting_tool, # First call: LLM requests tool
        final_llm_response_after_tool # Second call: LLM processes tool output
    ]

    # Mock the actual 'get_jira_issue' function in jira_tool.py
    # This ensures no real HTTP request is made by the tool.
    with patch('backend.app.tools.jira_tool.get_jira_issue') as mock_get_jira_issue:
        # Define what the mocked Jira tool should return
        mocked_jira_response_content = {
            "key": "TEST-123",
            "summary": "Mocked Summary",
            "status": "In Progress",
            "assignee": "Mock User",
            "url": "https://testjira.example.com/browse/TEST-123"
        }
        mock_get_jira_issue.return_value = json.dumps(mocked_jira_response_content)

        # Make the API call that should trigger the flow
        response = client.post("/api/prompt", json={"prompt": "Can you get Jira issue TEST-123?"})
        
        assert response.status_code == 200
        data = response.json()
        assert data["error"] is None
        assert data["response"] == "Jira issue TEST-123 summary is 'Mocked Summary'." # Final response from LLM

        # Verify that our mock Jira tool function was called correctly
        mock_get_jira_issue.assert_called_once_with("TEST-123")


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Check for a successful HTML response (content can be dynamic)
    assert response.headers["content-type"] == "text/html; charset=utf-8"
    assert "AI Agent Interface" in response.text # Check for a known string in index.html
