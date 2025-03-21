import openai
# OpenAI API Key
OPENAI_API_KEY = "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"
client = openai.OpenAI(api_key=OPENAI_API_KEY)
# Supply chain optimization calculation results(可以进一步修改：和solver联动，进行自动化读取)
optimal_transport = {
    "p1 → w1": 140000, "p1 → w2": 0, "p2 → w1": 0, "p2 → w2": 60000,
    "w1 → c1": 50000, "w1 → c2": 70000, "w1 → c3": 0, "w1 → c4": 20000,
    "w2 → c1": 0, "w2 → c2": 10000, "w2 → c3": 50000
}
total_cost = 740000

# Predefined What-If question template
WHAT_IF_QUESTIONS = """
1️⃣ **What would happen if the demand at market c1 increased by 10%?**
2️⃣ **What would happen if the demands at all market’s demond doubled?**
3️⃣ **Why are we using warehouse w2 for plant p1?**
4️⃣ **Can I use warehouse w1 only for market c3?**
5️⃣ **What if plant p2 can now supply only half of its original capacity?**
6️⃣ **The per-unit distribution cost from plant p2 to warehouse w1 is now $5. How does that affect the total cost?**
7️⃣ **Why does plant p1 produce more products for market c2 than for market c1?**
8️⃣ **Why does warehouse w2 receive more shipments from plant p2 than warehouse w1?**
9️⃣ **Why not only use one warehouse for all markets?**
"""

def ask_gpt(user_input, history):
    """GPT request combined with history"""
    chat_history = [{"role": "system", "content": "You're a supply chain assistant"}]

    # 添加历史对话
    for user_msg, ai_msg in history:
        chat_history.append({"role": "user", "content": user_msg})
        chat_history.append({"role": "assistant", "content": ai_msg})

    chat_history.append({"role": "user", "content": user_input})

    # build Prompt
    prompt = f"""
    You are a supply chain optimization assistant. Here are the results of the current optimization calculation:
    📌 **Supply chain decision variables**:
    {optimal_transport}
    📌 **Total transportation cost**:
    {total_cost}

    Your task:
    - Analyze the calculation results of supply chain optimization
    - Answer What-If questions from users
    - For What-If, You can refer to the following example question
    {WHAT_IF_QUESTIONS}

    Users'question:
    "{user_input}"

    Answer based on the supply chain optimization logic and provide the calculation process, not just the conclusion.
    """

    chat_history.append({"role": "system", "content": prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=chat_history
    )

    return response.choices[0].message.content

