# jarvondis/orchestrator/task_engine.py

class TaskEngine:
    def __init__(self, tools: dict):
        self.tools = tools

    def execute(self, message: str, context: dict) -> str:
        if "calculate" in message:
            return self.tools["math"].run(message)
        if "search" in message:
            return self.tools["web"].run(message)
        return self.default_chat(message, context)

    def default_chat(self, message: str, context: dict) -> str:
        # placeholder for LLM / rule-based response
        return f"You said: {message}"
