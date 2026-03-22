import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_text(prompt, max_tokens=100, temperature=0.7, top_p=1.0, n=1):
    """Generate text using the OpenAI GPT-3 model."""
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=max_tokens,
        n=n,
        stop=None,
        temperature=temperature,
        top_p=top_p,
    )
    return response.choices[0].text.strip()

def main():
    prompt = "Once upon a time, in a faraway land, there lived a powerful wizard who could..."
    generated_text = generate_text(prompt)
    print(generated_text)

if __name__ == "__main__":
    main()