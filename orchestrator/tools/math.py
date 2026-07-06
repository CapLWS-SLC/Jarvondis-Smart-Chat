class MathTool:
    """
    Safe math evaluator.
    Only supports basic arithmetic.
    """

    ALLOWED = set("0123456789+-*/(). ")

    def run(self, expression: str) -> str:
        cleaned = "".join(ch for ch in expression if ch in self.ALLOWED)

        try:
            result = eval(cleaned, {"__builtins__": None}, {})
            return str(result)
        except Exception:
            return "Math error."
