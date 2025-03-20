import openai

# OpenAI API Key
OPENAI_API_KEY = "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"

# new API structure
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def ask_gpt(prompt):
    """Call the GPT-4 API and return the AI-generated answer"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# test API
test_prompt = "Why is using multiple warehouses more efficient than using one warehouse in supply chain optimization?"
response = ask_gpt(test_prompt)
print("GPT-4 result:", response)