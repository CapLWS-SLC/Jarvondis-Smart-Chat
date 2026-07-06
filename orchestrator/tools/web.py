import requests

class WebTool:
    """
    Safe web utility tool.
    Does NOT execute arbitrary code or unsafe requests.
    Only allows GET requests to whitelisted domains.
    """

    WHITELIST = [
        "https://api.duckduckgo.com",
    ]

    def run(self, query: str) -> str:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"

        if not any(url.startswith(domain) for domain in self.WHITELIST):
            return "Blocked: domain not allowed."

        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            abstract = data.get("Abstract", "")
            if not abstract:
                return "No results found."
            return abstract
        except Exception:
            return "Web tool error."
