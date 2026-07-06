class TaskEngine:
    def __init__(self, registry):
        self.registry = registry

    def execute(self, message: str, context: dict) -> str:
        msg = message.lower()

        # Web search
        if msg.startswith("search "):
            query = msg.replace("search ", "")
            return self.registry.get("web").run(query)

        # Math
        if msg.startswith("calculate "):
            expr = msg.replace("calculate ", "")
            return self.registry.get("math").run(expr)

        # System info
        if msg.startswith("system "):
            cmd = msg.replace("system ", "")
            return self.registry.get("system").run(cmd)

        # NLP tools
        if msg.startswith("summarize "):
            text = msg.replace("summarize ", "")
            return self.registry.get("nlp").run("summarize", text)

        if msg.startswith("keywords "):
            text = msg.replace("keywords ", "")
            return self.registry.get("nlp").run("keywords", text)

        # Default fallback
        return f"[Jarvondis] {message}"
