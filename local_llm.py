import ollama

def generate(prompt: str, model: str) -> str:
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]
