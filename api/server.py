from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from jarvondis.core.engine import JarvondisEngine
from jarvondis.safety.filters import SafetyFilters
from jarvondis.policy.policy_engine import PolicyEngine, PolicyResult
from jarvondis.persona.persona_engine import PersonaEngine
from jarvondis.memory.memory_engine import MemoryEngine
from jarvondis.orchestrator.tools.tool_registry import ToolRegistry
from jarvondis.orchestrator.task_engine import TaskEngine

app = FastAPI(title="Jarvondis Smart Chat", version="1.0.0")

# Enable CORS for web frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    user_id: str = "anonymous"

class ChatResponse(BaseModel):
    response: str
    user_id: str

# Core modules initialization
safety = SafetyFilters()
policy = PolicyEngine(rules=[])
persona = PersonaEngine(profile={"tone_prefix": "[Jarvondis] "})
memory = MemoryEngine(store={})

# Task orchestrator setup
registry = ToolRegistry()
orchestrator = TaskEngine(registry)

# Main engine
engine = JarvondisEngine(safety, policy, persona, memory, orchestrator)

# API Routes
@app.get("/")
def root():
    """Root endpoint - API status"""
    return {"status": "running", "service": "Jarvondis Smart Chat"}

@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Main chat endpoint - process user message through safety and task engine"""
    try:
        response = engine.process(req.message)
        return ChatResponse(response=response, user_id=req.user_id)
    except Exception as e:
        return ChatResponse(response=f"Error processing message: {str(e)}", user_id=req.user_id)

@app.post("/search")
def search(req: ChatRequest):
    """Web search endpoint"""
    message = f"search {req.message}"
    response = engine.process(message)
    return ChatResponse(response=response, user_id=req.user_id)

@app.post("/calculate")
def calculate(req: ChatRequest):
    """Math calculation endpoint"""
    message = f"calculate {req.message}"
    response = engine.process(message)
    return ChatResponse(response=response, user_id=req.user_id)

@app.post("/summarize")
def summarize(req: ChatRequest):
    """Text summarization endpoint"""
    message = f"summarize {req.message}"
    response = engine.process(message)
    return ChatResponse(response=response, user_id=req.user_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
