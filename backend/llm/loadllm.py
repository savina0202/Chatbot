from config import MODEL_PROVIDER, OPENAI_API_KEY, OPENAI_MODEL, HF_MODEL


if MODEL_PROVIDER == "openai":
    import openai
    openai.api_key = OPENAI_API_KEY
    print(f"Using OpenAI model: {OPENAI_MODEL}\n")

    def llm_call(prompt, max_new_tokens=100):
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content']

elif MODEL_PROVIDER == "hf":
    from transformers import pipeline

    llm = pipeline("text-generation", model=HF_MODEL)
    print(f"Using Hugging Face model: {HF_MODEL}\n")

    def llm_call(prompt, max_new_tokens=100):
        outputs = llm(prompt, max_new_tokens=max_new_tokens)
        return outputs[0]["generated_text"]

else:
    raise ValueError(f"Unknown model provider: {MODEL_PROVIDER}")






