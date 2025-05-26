# AI Agent with LangGraph and Web UI

This project is a web application that uses a Large Language Model (LLM) orchestrated by LangGraph as its backend, with a simple webpage for user interaction.

## Project Structure

- `backend/`: Contains the FastAPI backend, LangGraph agent logic, and LLM connection.
- `frontend/`: Contains the HTML, CSS, and JavaScript for the user interface.

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
    Copy the `backend/.env.example` file to `backend/.env` and fill in your actual API keys or other configurations.
    ```bash
    cp .env.example .env
    ```
    Then edit `.env` with your details.

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
-   The frontend is served directly by FastAPI's static file handling for this basic setup.
-   Once the backend is running, open your web browser and navigate to `http://localhost:8000/` to view the `index.html` page.
    *(Note: We will need to adjust FastAPI to serve the frontend from the root or a more user-friendly path later)*

## Running Tests (Backend)
1.  Navigate to the `backend` directory.
2.  Ensure your virtual environment is activated and development dependencies (`pytest`, `httpx`) are installed.
3.  Run pytest:
    ```bash
    pytest
    ```

## Future Development
-   Implement actual LangGraph agent logic in `backend/app/agent.py`.
-   Connect to a real LLM via `backend/app/llm_config.py`.
-   Enhance frontend UI and UX.
-   Add more comprehensive error handling and input validation.
