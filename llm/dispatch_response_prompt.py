import json
from openai import OpenAI
from config import MY_API_KEY

# 初始化 OpenAI 客户端（使用新版 SDK）
client = OpenAI(api_key="")
# 加载 dispatch 调度 prompt 配置
with open("llm/dispatch_prompt_updated.json", "r") as f:
    dispatch_prompt = json.load(f)["dispatch_prompt"]

# 加载各类型 intent prompt 配置
with open("llm/supply_chain_prompts_english.json", "r") as f:
    intent_prompts = json.load(f)

# 保留最多三轮历史对话
def update_history(history, user_msg, ai_msg, max_len=3):
    history.append((user_msg, ai_msg))
    return history[-max_len:]

# 将历史格式化为prompt所需的文本
def format_history(history):
    return "\n".join([f"User: {u}\nAssistant: {a}" for u, a in history])

# 构造 dispatch prompt，使用 JSON 中的 role + instructions + inputs + examples
def build_dispatch_prompt(question, history):
    previous = format_history(history)
    input_values = {
        "{$previous_interactions}": previous,
        "{$QUESTION}": question
    }
    prompt = f"{dispatch_prompt['role']}\n{dispatch_prompt['task_instruction']}\n{dispatch_prompt['instructions']}\n\n"

    # 拼接 few-shot 示例
    for example in dispatch_prompt.get("examples", []):
        prompt += f"User Question: {example['User Question']}\nDispatch Response: {example['Dispatch Response']}\n\n"

    # 拼接当前 inputs
    for field in dispatch_prompt["inputs"]:
        field_value = input_values.get(field, "")
        prompt += f"{field.replace('{$', '').replace('}', '')}:\n{field_value}\n\n"

    prompt += "Intent Type:"
    return prompt

# 使用 GPT 模型分类意图类型
def classify_intent_from_prompt(question, history):
    prompt = build_dispatch_prompt(question, history)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    return response.choices[0].message.content.strip().lower()

# 构造意图类型的 prompt（computation/explanation 等）
def build_intent_prompt(intent_type, question, history):
    if intent_type not in intent_prompts:
        raise ValueError(f"Unknown intent type: {intent_type}")

    prompt_cfg = intent_prompts[intent_type]
    previous = format_history(history)
    input_values = {
        "{$previous_interactions}": previous,
        "{$QUESTION}": question
    }

    prompt = f"{prompt_cfg['role']}\n{prompt_cfg['task_instruction']}\n{prompt_cfg['instructions']}\n\n"
    for field in prompt_cfg["inputs"]:
        prompt += f"{field.replace('{$', '').replace('}', '')}:\n{input_values.get(field, '')}\n\n"

    return prompt

# ⛳ 主控流程函数：分类 → 拼接 prompt → GPT 回答 → 更新历史
def ask_supply_chain_assistant_final(question, history):
    intent_type = classify_intent_from_prompt(question, history)
    final_prompt = build_intent_prompt(intent_type, question, history)

    messages = [{"role": "system", "content": "You are a helpful supply chain assistant."}]
    messages.append({"role": "user", "content": final_prompt})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )

    ai_response = response.choices[0].message.content
    updated_history = update_history(history, question, ai_response)
    return intent_type, ai_response, updated_history