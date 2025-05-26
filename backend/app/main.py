from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from . import agent
from . import llm_config # To ensure it's loaded
import logging
import os # For path joining

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Determine the correct path to the frontend directory
# This assumes 'main.py' is in 'backend/app/' and 'frontend' is sibling to 'backend'
# Adjust if your structure is different or if run from a different working directory.
# For robustness, consider absolute paths or configuration-driven paths.
current_dir = os.path.dirname(os.path.realpath(__file__))
backend_dir = os.path.dirname(current_dir) # This should be the 'backend' directory
project_root_dir = os.path.dirname(backend_dir) # This should be the project root
frontend_static_dir = os.path.join(project_root_dir, "frontend", "static")
frontend_templates_dir = os.path.join(project_root_dir, "frontend", "templates")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory=frontend_static_dir), name="static")

agent_executor = agent.AgentExecutor(llm_config)

class PromptRequest(BaseModel):
    prompt: str

class PromptResponse(BaseModel):
    response: str = None
    error: str = None

@app.post("/api/prompt", response_model=PromptResponse)
async def handle_prompt(request: PromptRequest):
    try:
        response_text = await agent_executor.arun(prompt=request.prompt)
        if response_text is None:
             logger.warning(f"Agent returned None for prompt: {request.prompt}")
             return PromptResponse(error="Agent returned no response.")
        return PromptResponse(response=response_text)
    except Exception as e:
        logger.error(f"Error handling prompt '{request.prompt}': {e}", exc_info=True)
        return PromptResponse(error=f"An internal error occurred: {type(e).__name__}")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_html_path = os.path.join(frontend_templates_dir, "index.html")
    try:
        with open(index_html_path, "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        logger.error(f"index.html not found at {index_html_path}")
        raise HTTPException(status_code=404, detail="Frontend not found. Ensure index.html is in frontend/templates.")
    except Exception as e:
        logger.error(f"Error reading index.html: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Could not load frontend.")


# To run this app (from the 'backend' directory):
# uvicorn app.main:app --reload
