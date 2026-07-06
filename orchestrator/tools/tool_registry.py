from .web import WebTool
from .math import MathTool
from .system import SystemTool
from .nlp import NLPTool

class ToolRegistry:
    """
    Unified tool loader for Jarvondis.
    """

    def __init__(self):
        self.tools = {
            "web": WebTool(),
            "math": MathTool(),
            "system": SystemTool(),
            "nlp": NLPTool(),
        }

    def get(self, name: str):
        return self.tools.get(name)
