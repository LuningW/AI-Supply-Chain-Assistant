import pandas as pd
import numpy as np

# 原始数据读取和初始化
file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')
Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]
X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]
probabilities = data.iloc[:, 1:].values

# 原始情况利润计算（无重加工）
def original_profit(Q, X):
    if X <= 19:
        revenue = 300 * Q
        cost = 700 * Q
    elif 20 <= X <= 22:
        revenue = 20 * 2000 + 1500 * (X - 20) + 300 * (Q - X)
        cost = 700 * Q + 500 * X
    else:  # X >= 23
        revenue = 2000 * 20 + 1500 * 2 + 300 * (Q - 22)
        cost = 700 * Q + 500 * 22
    return revenue - cost

# 重加工情况利润计算
def rework_profit(Q, X, rework_cost):
    if X <= 19:
        rework_units = 20 - X
        revenue = 20 * 2000
        cost = 700 * Q + 500 * 20 + rework_cost * rework_units
    elif 20 <= X <= 22:
        revenue = 20 * 2000 + 1500 * (X - 20) + 300 * (Q - X)
        cost = 700 * Q + 500 * X
    else:  # X >= 23
        revenue = 2000 * 20 + 1500 * 2 + 300 * (Q - 22)
        cost = 700 * Q + 500 * 22
    return revenue - cost

# 30个问题设定
questions = [
    {"rework_cost": 120, "scheduled_qty": 22},
    {"rework_cost": 180, "scheduled_qty": 24},
    {"rework_cost": 230, "scheduled_qty": 20},
    {"rework_cost": 310, "scheduled_qty": 25},
    {"rework_cost": 150, "scheduled_qty": 21},
    {"rework_cost": 270, "scheduled_qty": 23},
    {"rework_cost": 390, "scheduled_qty": 22},
    {"rework_cost": 110, "scheduled_qty": 24},
    {"rework_cost": 440, "scheduled_qty": 20},
    {"rework_cost": 200, "scheduled_qty": 25},
    {"rework_cost": 330, "scheduled_qty": 21},
    {"rework_cost": 170, "scheduled_qty": 23},
    {"rework_cost": 290, "scheduled_qty": 22},
    {"rework_cost": 410, "scheduled_qty": 24},
    {"rework_cost": 130, "scheduled_qty": 20},
    {"rework_cost": 250, "scheduled_qty": 25},
    {"rework_cost": 370, "scheduled_qty": 21},
    {"rework_cost": 490, "scheduled_qty": 23},
    {"rework_cost": 140, "scheduled_qty": 22},
    {"rework_cost": 220, "scheduled_qty": 24},
    {"rework_cost": 350, "scheduled_qty": 20},
    {"rework_cost": 470, "scheduled_qty": 25},
    {"rework_cost": 160, "scheduled_qty": 21},
    {"rework_cost": 280, "scheduled_qty": 23},
    {"rework_cost": 400, "scheduled_qty": 22},
    {"rework_cost": 190, "scheduled_qty": 24},
    {"rework_cost": 320, "scheduled_qty": 20},
    {"rework_cost": 450, "scheduled_qty": 25},
    {"rework_cost": 240, "scheduled_qty": 21},
    {"rework_cost": 380, "scheduled_qty": 23}
]

# 准备结果DataFrame
results = []
for i, q in enumerate(questions, 1):
    rework_cost = q["rework_cost"]
    scheduled_qty = q["scheduled_qty"]
    
    # 计算原始条件下的期望利润（相同Q）
    original_expected = 0
    for idx, X in enumerate(X_values):
        profit = original_profit(scheduled_qty, X)
        original_expected += profit * probabilities[idx, Q_values.index(scheduled_qty)]
    
    # 计算重加工条件下的期望利润（相同Q）
    rework_expected = 0
    for idx, X in enumerate(X_values):
        profit = rework_profit(scheduled_qty, X, rework_cost)
        rework_expected += profit * probabilities[idx, Q_values.index(scheduled_qty)]
    
    profit_diff = rework_expected - original_expected
    
    # 构建严格符合要求的响应文本
    change = "increase" if profit_diff >= 0 else "decrease"
    scenario_desc = f"If we can pay ${rework_cost} to rework the bad castings per unit, what is the expected profit when the number of casting scheduled is {scheduled_qty}"
    chatgpt_response = f"chatgpt: If we can pay ${rework_cost} to rework the bad castings per unit and the number of casting scheduled is {scheduled_qty}, the expected profit is ${rework_expected:.2f} which is a {change} of ${abs(profit_diff):.2f}."
    deepseek_response = f"deepseek: If we can pay ${rework_cost} to rework the bad castings per unit and the number of casting scheduled is {scheduled_qty}, the expected profit is ${rework_expected:.2f} which is a {change} of ${abs(profit_diff):.2f}."
    
    # 每个问题添加9行记录
    results.append({
        "Problem Number": i,
        "Scenario Description": scenario_desc,
        "ChatGPT Response": chatgpt_response,
        "DeepSeek Response": deepseek_response
    })
    for _ in range(8):
        results.append({
            "Problem Number": i,
            "Scenario Description": "",
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# 保存结果
df = pd.DataFrame(results)
output_path = "plan-questions-set6_final.xlsx"
df.to_excel(output_path, index=False,
           columns=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])
print(f"结果已保存到 {output_path}，完全符合要求的响应格式")