# orchestrator/task_engine.py

class TaskEngine:
    def execute(self, message, context):
        if "calculate" in message:
            return self.tools["math"].run(message)
        if "search" in message:
            return self.tools["web"].run(message)
        return self.default_chat(message, context)
