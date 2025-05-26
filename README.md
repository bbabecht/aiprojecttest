# AI Agent with LangGraph and Web UI

This project is a web application that uses a Large Language Model (LLM) orchestrated by LangGraph as its backend, with a simple webpage for user interaction.

## Project Structure

- `backend/`: Contains the FastAPI backend, LangGraph agent logic, and LLM connection.
- `frontend/`: Contains the HTML, CSS, and JavaScript for the user interface.

## Agent Capabilities
- **Chat**: General conversation powered by an OpenAI LLM (e.g., GPT-4o-mini).
- **Jira Integration**: Can fetch details for a specific Jira issue using its ID or key (e.g., "Get details for issue PROJECT-123").

## Setup and Installation

### Prerequisites
- Python 3.8+
- Node.js (only if you plan to add complex frontend build steps, not required for current setup)

### Backend Setup
1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create a Python virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    -   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    -   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Set up environment variables:**
    Navigate to the `backend` directory. Copy the `backend/.env.example` file to `backend/.env` and fill in your actual API keys and configurations.
    ```bash
    # from project_root/backend directory
    cp .env.example .env
    ```
    Edit `backend/.env` with your details. It will look like this:
    ```
    # OpenAI LLM Configuration
    OPENAI_API_KEY="your_openai_api_key_here"
    OPENAI_MODEL_NAME="gpt-4o-mini" # Or your specific model identifier

    # Jira Configuration
    JIRA_API_KEY="your_jira_api_key_here"
    JIRA_BASE_URL="https://your-domain.atlassian.net"
    ```

## Running the Application

### 1. Run the Backend Server
-   Navigate to the `backend` directory (if not already there).
-   Ensure your virtual environment is activated.
-   Start the FastAPI server using Uvicorn:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```
    The backend will be accessible at `http://localhost:8000`.

### 2. Access the Frontend
-   The frontend is served directly by FastAPI.
-   Once the backend is running, open your web browser and navigate to `http://localhost:8000/` to view the `index.html` page.

## Running Tests (Backend)
1.  Navigate to the `backend` directory.
2.  Ensure your virtual environment is activated and development dependencies (`pytest`, `httpx`) are installed.
3.  Run pytest:
    ```bash
    pytest
    ```

## Future Development
- Connect to a real LLM via `backend/app/llm_config.py` (using the .env file).
- Enhance frontend UI and UX.
- Add more comprehensive error handling and input validation.
- Expand with more tools and more complex agentic logic.
