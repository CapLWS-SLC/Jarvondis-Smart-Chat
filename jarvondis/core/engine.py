# jarvondis/core/engine.py

class JarvondisEngine:
    def __init__(self, safety, policy, persona, memory, orchestrator):
        self.safety = safety
        self.policy = policy
        self.persona = persona
        self.memory = memory
        self.orchestrator = orchestrator

    def process(self, user_message: str) -> str:
        if not self.safety.validate(user_message):
            return self.safety.block(user_message)

        policy_result = self.policy.apply(user_message)
        if policy_result.blocked:
            return policy_result.message

        styled_message = self.persona.apply_style(user_message)
        context = self.memory.retrieve_context(styled_message)
        response = self.orchestrator.execute(styled_message, context)
        self.memory.update(user_message, response)
        return response
