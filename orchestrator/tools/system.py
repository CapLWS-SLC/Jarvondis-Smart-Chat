import platform
import datetime

class SystemTool:
    """
    Safe system information tool.
    Does NOT execute shell commands.
    """

    def run(self, command: str) -> str:
        if "time" in command.lower():
            return f"Current system time: {datetime.datetime.now()}"
        if "os" in command.lower():
            return f"Operating system: {platform.system()} {platform.release()}"
        return "Unknown system command."
