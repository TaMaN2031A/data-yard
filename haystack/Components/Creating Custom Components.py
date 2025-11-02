from haystack import component

@component
class WelcomeTextGenerator:
    """A component generating personal welcome message and making it
    upper case."""
    @component.output_types(welcome_text=str, note=str)
    def run(self, name: str):
        return {"welcome_text": f'Hello {name}, welcome to Haystack!'.upper(),
                "note": "welcome message is ready"}