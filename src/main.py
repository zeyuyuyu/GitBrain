import openai

class CodeGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key

    def generate_code(self, prompt, max_tokens=2048, temperature=0.7):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=temperature,
        )

        return response.choices[0].text.strip()

if __name__ == "__main__":
    api_key = "your_openai_api_key_here"
    generator = CodeGenerator(api_key)
    prompt = "Write a Python function that calculates the factorial of a given number."
    generated_code = generator.generate_code(prompt)
    print(generated_code)