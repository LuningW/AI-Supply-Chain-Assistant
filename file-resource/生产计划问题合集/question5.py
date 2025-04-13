import pandas as pd
import numpy as np

# 原始数据读取和初始化
file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')
Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]
X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]
probabilities = data.iloc[:, 1:].values

# 原始条件（接受2个额外铸件）
def original_profit(Q, X):
    if X <= 19:
        revenue = 300 * Q
        cost = 700 * Q
    elif 20 <= X <= 22:
        revenue = 20 * 2000 +1500 * (X - 20)+ 300 * (Q - X)
        cost = 700 * Q + 500 * X
    else:
        revenue = 2000 * 20 +1500 * 2+ 300 * (Q - 22)
        cost = 700 * Q + 500 * 22
    return revenue - cost

# 计算原始最优解和利润
original_results = {}
for Q in Q_values:
    expected_profit = 0
    for i, X in enumerate(X_values):
        profit = original_profit(Q, X)
        expected_profit += profit * probabilities[i, Q_values.index(Q)]
    original_results[Q] = expected_profit
original_optimal_Q = max(original_results, key=original_results.get)
original_max_profit = original_results[original_optimal_Q]

# 30个问题设定
questions = [
    {"value1": 3, "value2": 12}, {"value1": 4, "value2": 15}, {"value1": 5, "value2": 18},
    {"value1": 6, "value2": 11}, {"value1": 3, "value2": 14}, {"value1": 4, "value2": 17},
    {"value1": 5, "value2": 10}, {"value1": 6, "value2": 19}, {"value1": 3, "value2": 16},
    {"value1": 4, "value2": 13}, {"value1": 5, "value2": 20}, {"value1": 6, "value2": 12},
    {"value1": 3, "value2": 15}, {"value1": 4, "value2": 18}, {"value1": 5, "value2": 11},
    {"value1": 6, "value2": 14}, {"value1": 3, "value2": 17}, {"value1": 4, "value2": 10},
    {"value1": 5, "value2": 19}, {"value1": 6, "value2": 16}, {"value1": 3, "value2": 13},
    {"value1": 4, "value2": 20}, {"value1": 5, "value2": 12}, {"value1": 6, "value2": 15},
    {"value1": 3, "value2": 18}, {"value1": 4, "value2": 11}, {"value1": 5, "value2": 14},
    {"value1": 6, "value2": 17}, {"value1": 3, "value2": 20}, {"value1": 4, "value2": 12}
]

# 新利润计算函数（考虑额外铸件和折扣）
def new_profit(Q, X, max_additional, discount_rate):
    discount_factor = 1 - discount_rate/100
    if X <= 19:
        revenue = 300 * Q
        cost = 700 * Q
    elif 20 <= X <= (20 + max_additional):
        revenue = 20 * 2000 * discount_factor + (X - 20) * 1500 * discount_factor + 300 * (Q - X)
        cost = 700 * Q + 500 * X
    else:
        revenue = 20 * 2000 * discount_factor + max_additional * 1500 * discount_factor + 300 * (Q - 20 - max_additional)
        cost = 700 * Q + 500 * (20 + max_additional)
    return revenue - cost

# 准备结果DataFrame
results = []
for i, q in enumerate(questions, 1):
    max_additional = q["value1"]
    discount_rate = q["value2"]
    
    # 计算新条件下的最优解
    current_results = {}
    for Q in Q_values:
        expected_profit = 0
        for idx, X in enumerate(X_values):
            profit = new_profit(Q, X, max_additional, discount_rate)
            expected_profit += profit * probabilities[idx, Q_values.index(Q)]
        current_results[Q] = expected_profit
    
    optimal_Q = max(current_results, key=current_results.get)
    max_profit = current_results[optimal_Q]
    profit_diff = max_profit - original_max_profit
    
    # 构建响应文本
    change = "increase" if profit_diff >= 0 else "decrease"
    scenario_desc = f"What if the customer accepts a maximum of {max_additional} additional castings with the total {discount_rate}% price reduction?"
    chatgpt_response = f"When the customer can accept a maximum of {max_additional} additional castings with the total {discount_rate}% price reduction, the maximum expected profit is ${max_profit:.2f}, which is a {change} of ${abs(profit_diff):.2f} compared to the original value."
    deepseek_response = f"When the customer can accept a maximum of {max_additional} additional castings with the total {discount_rate}% price reduction, the maximum expected profit is ${max_profit:.2f}, which is a {change} of ${abs(profit_diff):.2f} compared to the original value."
    
    # 每个问题添加9行记录
    for _ in range(9):
        results.append({
            "Problem Number": i,
            "Scenario Description": scenario_desc if _ == 0 else "",  # 只有第一行保留问题描述
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# 创建DataFrame并保存
df = pd.DataFrame(results)
df.to_excel("plan-questions-set5.xlsx", index=False, 
            columns=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])

print("结果已保存到 plan-questions-set5.xlsx")