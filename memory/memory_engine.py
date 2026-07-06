# jarvondis/memory/memory_engine.py

class MemoryEngine:
    def __init__(self, store):
        self.store = store

    def retrieve_context(self, message: str) -> dict:
        # TODO: implement embeddings / similarity
        return {"history": []}

    def update(self, user_message: str, response: str) -> None:
        # TODO: append to store, persist if needed
        pass
