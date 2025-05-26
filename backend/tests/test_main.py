from fastapi.testclient import TestClient
from ..app.main import app # Adjusted import path

client = TestClient(app)

def test_handle_prompt_success():
    # Test with a valid prompt that should return the dummy response
    response = client.post("/api/prompt", json={"prompt": "Hello agent"})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data # Check if 'response' key exists
    assert data["response"] is not None # Check if 'response' is not null
    assert "This is a dummy response to your prompt: 'Hello agent'" in data["response"]
    assert data["error"] is None

def test_handle_prompt_empty_prompt():
    # Test with an empty prompt string (optional, based on how you want to handle it)
    # Assuming current dummy agent handles it gracefully
    response = client.post("/api/prompt", json={"prompt": ""})
    assert response.status_code == 200 # Or 422 if you add validation for empty prompt
    data = response.json()
    assert "response" in data
    assert "This is a dummy response to your prompt: ''" in data["response"] # Current dummy behavior
    assert data["error"] is None

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "AI Agent Backend is running."}

# Example of how to test an error case if the agent could raise a specific error
# For now, this is harder to test without more complex agent logic or mocking
# def test_handle_prompt_agent_error():
#     # This would require mocking the agent_executor to raise an exception
#     # from unittest.mock import patch
#     # with patch('backend.app.main.agent_executor.arun', side_effect=Exception("Test agent error")):
#     #     response = client.post("/api/prompt", json={"prompt": "trigger error"})
#     #     assert response.status_code == 200 # Because our main handler catches it
#     #     data = response.json()
#     #     assert data["response"] is None
#     #     assert "An internal error occurred: Exception" in data["error"] # Matches the generic error
