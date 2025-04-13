import pandas as pd
import numpy as np
from openpyxl import Workbook

# 读取原始Excel数据
file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# 提取Q值和X值
Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]  # 获取Q的值
X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]  # 获取X的值
probabilities = data.iloc[:, 1:].values

# 原始条件（$700/unit）的基准利润计算
def calculate_original_profit(Q, X):
    if X < 20:
        revenue = 300 * Q
        cost = 700 * Q
    elif 20 <= X <= 22:
        revenue = 20 * 2000 + 1500 * (X - 20) + 300 * (Q - X)
        cost = 700 * Q + 500 * X
    else:
        revenue = 20 * 2000 + 1500 * 2 + 300 * (Q - 22)
        cost = 700 * Q + 500 * 22
    return revenue - cost

# 计算原始最优解和利润
original_profits = {}
for Q in Q_values:
    expected_profit = 0
    for i, X in enumerate(X_values):
        profit = calculate_original_profit(Q, X)
        expected_profit += profit * probabilities[i, Q_values.index(Q)]
    original_profits[Q] = round(expected_profit, 2)

original_optimal_Q = max(original_profits, key=original_profits.get)
original_max_profit = original_profits[original_optimal_Q]

# 使用之前生成的30个问题（铸造成本变化）
cost_scenarios = [
    (1, "The per-unit casting cost is now $540. How does that affect the profit?", 540),
    (2, "The per-unit casting cost is now $890. How does that affect the profit?", 890),
    (3, "The per-unit casting cost is now $620. How does that affect the profit?", 620),
    (4, "The per-unit casting cost is now $970. How does that affect the profit?", 970),
    (5, "The per-unit casting cost is now $550. How does that affect the profit?", 550),
    (6, "The per-unit casting cost is now $830. How does that affect the profit?", 830),
    (7, "The per-unit casting cost is now $580. How does that affect the profit?", 580),
    (8, "The per-unit casting cost is now $920. How does that affect the profit?", 920),
    (9, "The per-unit casting cost is now $660. How does that affect the profit?", 660),
    (10, "The per-unit casting cost is now $780. How does that affect the profit?", 780),
    (11, "The per-unit casting cost is now $510. How does that affect the profit?", 510),
    (12, "The per-unit casting cost is now $950. How does that affect the profit?", 950),
    (13, "The per-unit casting cost is now $530. How does that affect the profit?", 530),
    (14, "The per-unit casting cost is now $880. How does that affect the profit?", 880),
    (15, "The per-unit casting cost is now $590. How does that affect the profit?", 590),
    (16, "The per-unit casting cost is now $840. How does that affect the profit?", 840),
    (17, "The per-unit casting cost is now $650. How does that affect the profit?", 650),
    (18, "The per-unit casting cost is now $990. How does that affect the profit?", 990),
    (19, "The per-unit casting cost is now $560. How does that affect the profit?", 560),
    (20, "The per-unit casting cost is now $810. How does that affect the profit?", 810),
    (21, "The per-unit casting cost is now $500. How does that affect the profit?", 500),
    (22, "The per-unit casting cost is now $930. How does that affect the profit?", 930),
    (23, "The per-unit casting cost is now $570. How does that affect the profit?", 570),
    (24, "The per-unit casting cost is now $860. How does that affect the profit?", 860),
    (25, "The per-unit casting cost is now $630. How does that affect the profit?", 630),
    (26, "The per-unit casting cost is now $980. How does that affect the profit?", 980),
    (27, "The per-unit casting cost is now $520. How does that affect the profit?", 520),
    (28, "The per-unit casting cost is now $850. How does that affect the profit?", 850),
    (29, "The per-unit casting cost is now $600. How does that affect the profit?", 600),
    (30, "The per-unit casting cost is now $1000. How does that affect the profit?", 1000)
]

# 准备结果存储(每个问题9行)
results = []

for problem_num, description, new_cost in cost_scenarios:
    expected_profits = {}
    
    # 计算每个Q的期望利润（新成本）
    for Q in Q_values:
        expected_profit = 0
        for i, X in enumerate(X_values):
            # 修改后的利润计算函数（仅改变铸造成本）
            if X < 20:
                revenue = 300 * Q
                cost = new_cost * Q
            elif 20 <= X <= 22:
                revenue = 20 * 2000 + 1500 * (X - 20) + 300 * (Q - X)
                cost = new_cost * Q + 500 * X
            else:
                revenue = 20 * 2000 + 1500 * 2 + 300 * (Q - 22)
                cost = new_cost * Q + 500 * 22
                
            profit = revenue - cost
            expected_profit += profit * probabilities[i, Q_values.index(Q)]
        
        expected_profits[Q] = round(expected_profit, 2)
    
    # 找到最优解
    optimal_Q = max(expected_profits, key=expected_profits.get)
    max_profit = expected_profits[optimal_Q]
    
    # 计算利润变化
    profit_diff = max_profit - original_max_profit
    change_type = "increase" if profit_diff >= 0 else "decrease"
    abs_diff = abs(profit_diff)
    
    # 格式化响应
    chatgpt_response = (
        f"chatgpt: When the per-unit casting cost has become ${new_cost}, "
        f"the maximum expected profit is ${max_profit}, which is a {change_type} "
        f"of ${abs_diff} compared to the original value (${original_max_profit})."
    )
    
    deepseek_response = (
        f"deepseek: When the per-unit casting cost has become ${new_cost}, "
        f"the maximum expected profit is ${max_profit}, which is a {change_type} "
        f"of ${abs_diff} compared to the original value (${original_max_profit})."
    )
    
    # 为每个问题添加9行相同的结果
    for _ in range(9):
        results.append({
            "Problem Number": problem_num,
            "Scenario Description": description,
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# 创建DataFrame并保存到Excel
columns_order = ["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"]
df = pd.DataFrame(results, columns=columns_order)

output_path = 'plan-questions-set3.xlsx'
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, header=True)

print(f"结果已保存到 {output_path}")
print(f"总行数: {len(df)} (30个问题 × 每个问题9行)")