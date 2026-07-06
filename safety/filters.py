# safety/filters.py

class SafetyFilters:
    def validate(self, message):
        return all([
            not self.contains_harm(message),
            not self.contains_illegal(message),
            not self.contains_sensitive_data(message),
            not self.contains_child_endangerment(message)
        ])

    def block(self, message):
        return "Message blocked for safety reasons."

    def contains_harm(self, msg): ...
    def contains_illegal(self, msg): ...
    def contains_sensitive_data(self, msg): ...
    def contains_child_endangerment(self, msg): ...
