class NLPTool:
    """
    Basic text utilities: summarization, keyword extraction, formatting.
    """

    def summarize(self, text: str) -> str:
        sentences = text.split(".")
        if len(sentences) < 2:
            return text
        return sentences[0] + "."

    def keywords(self, text: str) -> str:
        words = text.split()
        keywords = [w for w in words if len(w) > 6]
        return ", ".join(keywords[:10])

    def run(self, command: str, text: str = "") -> str:
        if "summarize" in command.lower():
            return self.summarize(text)
        if "keywords" in command.lower():
            return self.keywords(text)
        return "Unknown NLP command."
