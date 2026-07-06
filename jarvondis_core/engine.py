# jarvondis_core/engine.py

class JarvondisEngine:
    def __init__(self, safety, policy, persona, memory, orchestrator):
        self.safety = safety
        self.policy = policy
        self.persona = persona
        self.memory = memory
        self.orchestrator = orchestrator

    def process(self, user_message):
        # 1. Safety check
        if not self.safety.validate(user_message):
            return self.safety.block(user_message)

        # 2. Policy enforcement
        policy_result = self.policy.apply(user_message)
        if policy_result.blocked:
            return policy_result.message

        # 3. Persona shaping
        styled_message = self.persona.apply_style(user_message)

        # 4. Memory integration
        context = self.memory.retrieve_context(styled_message)

        # 5. Task orchestration
        response = self.orchestrator.execute(styled_message, context)

        # 6. Memory update
        self.memory.update(user_message, response)

        return response
