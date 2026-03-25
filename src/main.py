import openai
import os

API_KEY = os.environ.get('OPENAI_API_KEY')

def generate_code_suggestions(prompt):
    """
    Generate code suggestions using the OpenAI API.
    
    Args:
        prompt (str): The prompt to use for generating code suggestions.
    
    Returns:
        str: The generated code suggestions.
    """
    openai.api_key = API_KEY
    
    response = openai.Completion.create(
        engine="davinci\