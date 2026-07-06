# memory/memory_engine.py

class MemoryEngine:
    def retrieve_context(self, message):
        # embeddings + similarity search
        return self.search(message)

    def update(self, user_message, response):
        # store relevant facts
        pass
