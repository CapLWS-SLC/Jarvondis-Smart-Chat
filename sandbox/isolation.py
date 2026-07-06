# sandbox/isolation.py

class Sandbox:
    def run(self, plugin, data):
        try:
            return plugin.execute(data)
        except Exception:
            return "Plugin execution blocked for safety."
