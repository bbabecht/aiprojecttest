from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool, tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, BaseMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # For potential future use with memory

from typing import TypedDict, Annotated, Sequence
import operator # For StateGraph

from . import llm_config # For OpenAI API key and model
from .tools.jira_tool import get_jira_issue # Import the Jira tool function

# --- 1. Initialize LLM and Tools ---
# Initialize LLM
# Ensure OPENAI_API_KEY and OPENAI_MODEL_NAME are set in your .env file
llm = ChatOpenAI(
    api_key=llm_config.OPENAI_API_KEY,
    model=llm_config.OPENAI_MODEL_NAME,
    temperature=0.7 # Adjust temperature as needed
)

# Create Langchain Tool for Jira
jira_tool = Tool(
    name="get_jira_issue_details", # Name for the LLM to refer to this tool
    func=get_jira_issue,
    description="Fetches details for a specific Jira issue using its ID or key (e.g., 'PROJECT-123'). Returns key, summary, status, assignee, and URL of the issue."
)

tools = [jira_tool]

# --- 2. Define Agent State ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # You can add other fields here if needed for more complex states

# --- 3. Define Agent Nodes ---

# Node to call the LLM
def call_model_node(state: AgentState):
    """Invokes the LLM with the current state's messages."""
    print(f"--- Calling LLM with messages: {state['messages']} ---")
    # The .bind_tools() method makes the LLM aware of the available tools and their schemas.
    # This allows the LLM to decide if it needs to call a tool.
    response = llm.bind_tools(tools).invoke(state['messages'])
    print(f"--- LLM Response: {response} ---")
    return {"messages": [response]}

# Node to execute tools
def tool_node(state: AgentState):
    """Executes the tool called by the LLM, if any."""
    last_message = state['messages'][-1]
    if not isinstance(last_message, AIMessage) or not last_message.tool_calls:
        # No tool call, pass through
        return {"messages": []}

    tool_messages = []
    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        print(f"--- Executing Tool: {tool_name} with args: {tool_args} ---")
        
        selected_tool = None
        for t in tools:
            if t.name == tool_name:
                selected_tool = t
                break
        
        if not selected_tool:
            error_msg = f"Error: Tool '{tool_name}' not found."
            print(error_msg)
            tool_messages.append(ToolMessage(content=error_msg, tool_call_id=tool_call["id"]))
            continue

        try:
            # Assuming the tool's func takes arguments as a dictionary or directly if only one arg.
            # Our get_jira_issue takes a single string arg.
            # If the LLM provides args as a dict like {"issue_id_or_key": "val"}, extract it.
            if isinstance(tool_args, dict) and len(tool_args) == 1:
                tool_response = selected_tool.invoke(list(tool_args.values())[0])
            else: # Fallback or if args are directly the value
                tool_response = selected_tool.invoke(tool_args)
                
        except Exception as e:
            tool_response = f"Error executing tool {tool_name}: {e}"
        
        print(f"--- Tool Response ({tool_name}): {tool_response} ---")
        tool_messages.append(ToolMessage(content=str(tool_response), tool_call_id=tool_call["id"]))
        
    return {"messages": tool_messages}

# --- 4. Define Edges ---
def should_continue_or_end(state: AgentState):
    """Determines whether to continue with another LLM call (if a tool was called) or end."""
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        # If the LLM made a tool call, continue to the tool_node
        return "continue_to_tool"
    # Otherwise, the LLM provided a direct answer, so end
    return END

# --- 5. Compile the Graph ---
# Using MemorySaver for potential future state persistence, though not strictly required for current setup.
# memory = MemorySaver() # If you want to add checkpointers
workflow = StateGraph(AgentState)

workflow.add_node("llm_call", call_model_node)
workflow.add_node("tool_executor", tool_node)

workflow.set_entry_point("llm_call")

workflow.add_conditional_edges(
    "llm_call", # Source node
    should_continue_or_end, # Function to decide the next path
    {
        "continue_to_tool": "tool_executor", # If "continue_to_tool", go to tool_executor
        END: END  # If END, finish the graph execution
    }
)
workflow.add_edge("tool_executor", "llm_call") # After tool execution, go back to LLM

# Compile the graph into a runnable agent
# app_runnable = workflow.compile(checkpointer=memory) # If using memory/checkpoints
app_runnable = workflow.compile()

# --- 6. Update AgentExecutor Class ---
class AgentExecutor:
    def __init__(self, llm_config_arg_not_used_anymore=None): # llm_config arg is no longer directly used here as llm is global
        self.runnable = app_runnable
        # You might want to pass 'llm_config' if other parts of the agent needed it,
        # but for this setup, 'llm' and 'tools' are defined in the module scope.

    async def arun(self, prompt: str):
        """Runs the agent with the given prompt."""
        print(f"--- AgentExecutor.arun received prompt: {prompt} ---")
        # LangGraph expects a dictionary input matching the AgentState structure.
        # For a new conversation, messages would typically be just the HumanMessage.
        inputs = {"messages": [HumanMessage(content=prompt)]}
        
        # The .stream() method can be used for streaming responses.
        # For a single response, .invoke() is simpler.
        # Let's use .invoke() for now and extract the final response.
        final_state = self.runnable.invoke(inputs)
        
        # The final response from the LLM will be the last AIMessage in the messages list
        # that does not have a tool_call.
        response_message = "No response generated." # Default
        for msg in reversed(final_state['messages']):
            if isinstance(msg, AIMessage) and not msg.tool_calls:
                response_message = msg.content
                break
        
        print(f"--- AgentExecutor.arun final response: {response_message} ---")
        return response_message

# Placeholder for old get_agent_response (can be removed)
# def get_agent_response(prompt: str) -> str:
#     print(f"Agent received prompt: {prompt}")
#     return f"This is a dummy response to your prompt: '{prompt}'"
