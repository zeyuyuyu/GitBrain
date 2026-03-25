import os
import openai

class LLMIntegration:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_text(self, prompt, max_tokens=2048, temperature=0.7):
        response = openai.Completion.create(
            engine="text-davinci-002\