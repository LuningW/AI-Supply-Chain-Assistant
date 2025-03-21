import openai
from config import MY_API_KEY

# OpenAI API Key
OPENAI_API_KEY = MY_API_KEY

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