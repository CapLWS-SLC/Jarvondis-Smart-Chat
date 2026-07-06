# persona/persona_engine.py

class PersonaEngine:
    def __init__(self, profile):
        self.profile = profile

    def apply_style(self, message):
        return f"{self.profile['tone_prefix']} {message}"
