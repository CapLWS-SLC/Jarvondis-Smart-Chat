# jarvondis/policy/policy_engine.py

class PolicyResult:
    def __init__(self, allowed: bool, message: str = ""):
        self.allowed = allowed
        self.blocked = not allowed
        self.message = message


class PolicyEngine:
    def __init__(self, rules):
        self.rules = rules

    def apply(self, message: str) -> PolicyResult:
        for rule in self.rules:
            result = rule.evaluate(message)
            if result.blocked:
                return result
        return PolicyResult(allowed=True)
