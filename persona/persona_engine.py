# jarvondis/persona/persona_engine.py

class PersonaEngine:
    def __init__(self, profile: dict):
        self.profile = profile

    def apply_style(self, message: str) -> str:
        prefix = self.profile.get("tone_prefix", "")
        return f"{prefix}{message}"
