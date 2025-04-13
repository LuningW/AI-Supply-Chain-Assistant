import pandas as pd
import numpy as np

# 原始数据读取和初始化（假设与之前相同）
file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')
Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]
X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]
probabilities = data.iloc[:, 1:].values

# 原始回收价值（¥300）下的最优解和最大期望利润
original_recycle = 300

def calculate_profit(Q, X, recycle_value):
    if X <= 19:
        revenue = recycle_value * Q
        cost = 700 * Q
    elif 20 <= X <= 22:
        revenue = 20 * 2000 + 1500 * (X - 20) + recycle_value * (Q - X)
        cost = 700 * Q + 500 * X
    else:
        revenue = 2000 * 20 + 1500 * 2 + recycle_value * (Q - 22)
        cost = 700 * Q + 500 * 22
    return revenue - cost

# 计算原始最优解和利润
original_results = {}
for Q in Q_values:
    expected_profit = 0
    for i, X in enumerate(X_values):
        profit = calculate_profit(Q, X, original_recycle)
        expected_profit += profit * probabilities[i, Q_values.index(Q)]
    original_results[Q] = expected_profit
original_optimal_Q = max(original_results, key=original_results.get)
original_max_profit = original_results[original_optimal_Q]

# 30个问题设定
questions = [
    {"value": 0}, {"value": 10}, {"value": 20}, {"value": 30}, {"value": 40},
    {"value": 50}, {"value": 60}, {"value": 70}, {"value": 80}, {"value": 90},
    {"value": 100}, {"value": 110}, {"value": 120}, {"value": 130}, {"value": 140},
    {"value": 150}, {"value": 160}, {"value": 170}, {"value": 180}, {"value": 190},
    {"value": 200}, {"value": 5}, {"value": 25}, {"value": 45}, {"value": 65},
    {"value": 85}, {"value": 105}, {"value": 125}, {"value": 145}, {"value": 175}
]

# 准备结果DataFrame
results = []
for i, q in enumerate(questions, 1):
    recycle_value = q["value"]
    
    # 计算新回收价值下的最优解
    current_results = {}
    for Q in Q_values:
        expected_profit = 0
        for idx, X in enumerate(X_values):
            profit = calculate_profit(Q, X, recycle_value)
            expected_profit += profit * probabilities[idx, Q_values.index(Q)]
        current_results[Q] = expected_profit
    
    optimal_Q = max(current_results, key=current_results.get)
    max_profit = current_results[optimal_Q]
    profit_diff = max_profit - original_max_profit
    
    # 构建响应文本
    change = "increase" if profit_diff >= 0 else "decrease"
    chatgpt_response = f"When the recycle price has become ${recycle_value} per unit, the maximum expected profit is ${max_profit:.2f}, which is a {change} of ${abs(profit_diff):.2f} compared to the original value."
    deepseek_response = f"When the recycle price has become ${recycle_value} per unit, the maximum expected profit is ${max_profit:.2f}, which is a {change} of ${abs(profit_diff):.2f} compared to the original value."
    
    # 每个问题添加9行相同记录
    for _ in range(9):
        results.append({
            "Problem Number": i,
            "Scenario Description": f"What effect will this have if recycle value drops to ${recycle_value} per unit?",
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# 创建DataFrame并保存
df = pd.DataFrame(results)
df.to_excel("plan-questions-set4.xlsx", index=False, 
            columns=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])

print("结果已保存到 plan-questions-set4.xlsx")