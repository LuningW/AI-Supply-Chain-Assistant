import openai
import json
from dispatch_response_prompt import ask_supply_chain_assistant_final

# 设置 API 密钥
client = openai.OpenAI(api_key="")  # 🔁 替换为你的 key

if __name__ == "__main__":
    # 初始化对话历史为空
    history = []

    # 输入问题（你可以换成其它问题测试）
    question = "Why does warehouse w2 receive more shipments than w1?"

    # 调用主流程
    intent, response, history = ask_supply_chain_assistant_final(question, history)

    # 输出结果
    print("🔍 分类结果（Intent Type）:", intent)
    print("\n🧠 GPT 回复内容：\n", response)

"""
# 测试dispatch prompt
# 加载 prompt 配置
with open("llm/dispatch_prompt_updated.json", "r") as f:
    prompt_config = json.load(f)["dispatch_prompt"]

# 用户输入
user_question = "What would happen if the demand at market c1 increased by 10%?"
inputs = {
    "{$QUESTION}": user_question,
    "{$previous_interactions}": "",
    "{$background}": "",
    "{$scenario_description}": ""
}

# 构造 prompt
prompt_text = (
    f"{prompt_config['role']}\n\n"
    f"{prompt_config['task_instruction']}\n\n"
    f"Instructions: {prompt_config['instructions']}\n\n"
)

for ex in prompt_config["examples"]:
    prompt_text += f"Question: {ex['User Question']}\n"
    prompt_text += f"Answer: {ex['Dispatch Response']}\n\n"

prompt_text += f"Question: {inputs['{$QUESTION}']}\n"
prompt_text += "Answer:"

# 使用新版 API 发送请求
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": prompt_text}
    ],
    temperature=0
)

# 打印结果
intent_type = response.choices[0].message.content.strip()
print("🔍 Detected intent type:", intent_type)
"""