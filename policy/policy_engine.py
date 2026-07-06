# policy/policy_engine.py

class PolicyEngine:
    def __init__(self, rule_sets):
        self.rules = rule_sets

    def apply(self, message):
        for rule in self.rules:
            result = rule.evaluate(message)
            if result.blocked:
                return result
        return PolicyResult(allowed=True)
