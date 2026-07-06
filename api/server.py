# jarvondis/api/server.py

from fastapi import FastAPI
from pydantic import BaseModel

from jarvondis.core.engine import JarvondisEngine
from jarvondis.safety.filters import SafetyFilters
from jarvondis.policy.policy_engine import PolicyEngine, PolicyResult
from jarvondis.persona.persona_engine import PersonaEngine
from jarvondis.memory.memory_engine import MemoryEngine
from jarvondis.orchestrator.task_engine import TaskEngine

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


# minimal wiring
safety = SafetyFilters()
policy = PolicyEngine(rules=[])
persona = PersonaEngine(profile={"tone_prefix": "[Jarvondis] "})
memory = MemoryEngine(store={})
orchestrator = TaskEngine(tools={})
engine = JarvondisEngine(safety, policy, persona, memory, orchestrator)


@app.post("/chat")
def chat(req: ChatRequest):
    return {"response": engine.process(req.message)}
