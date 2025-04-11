import pandas as pd
import numpy as np
from openpyxl import Workbook

# 读取原始Excel数据
file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
data = pd.read_excel(file_path, sheet_name='Sheet1')

# 提取Q和X值
Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]
X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]
probabilities = data.iloc[:, 1:].values

# 原始条件（$2000/unit）的基准利润计算
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

# 新支付价格场景（$30增量）
payment_scenarios = [
    (1, "What would happen if the customer wants to pay $1530 per casting for 20 acceptable castings?", 1530),
    (2, "What would happen if the customer wants to pay $2970 per casting for 20 acceptable castings?", 2970),
    (3, "What would happen if the customer wants to pay $1710 per casting for 20 acceptable castings?", 1710),
    (4, "What would happen if the customer wants to pay $2370 per casting for 20 acceptable castings?", 2370),
    (5, "What would happen if the customer wants to pay $1650 per casting for 20 acceptable castings?", 1650),
    (6, "What would happen if the customer wants to pay $2850 per casting for 20 acceptable castings?", 2850),
    (7, "What would happen if the customer wants to pay $1830 per casting for 20 acceptable castings?", 1830),
    (8, "What would happen if the customer wants to pay $2430 per casting for 20 acceptable castings?", 2430),
    (9, "What would happen if the customer wants to pay $1950 per casting for 20 acceptable castings?", 1950),
    (10, "What would happen if the customer wants to pay $2730 per casting for 20 acceptable castings?", 2730),
    (11, "What would happen if the customer wants to pay $2070 per casting for 20 acceptable castings?", 2070),
    (12, "What would happen if the customer wants to pay $2550 per casting for 20 acceptable castings?", 2550),
    (13, "What would happen if the customer wants to pay $2190 per casting for 20 acceptable castings?", 2190),
    (14, "What would happen if the customer wants to pay $2610 per casting for 20 acceptable castings?", 2610),
    (15, "What would happen if the customer wants to pay $2250 per casting for 20 acceptable castings?", 2250),
    (16, "What would happen if the customer wants to pay $1890 per casting for 20 acceptable castings?", 1890),
    (17, "What would happen if the customer wants to pay $1590 per casting for 20 acceptable castings?", 1590),
    (18, "What would happen if the customer wants to pay $2910 per casting for 20 acceptable castings?", 2910),
    (19, "What would happen if the customer wants to pay $1770 per casting for 20 acceptable castings?", 1770),
    (20, "What would happen if the customer wants to pay $2310 per casting for 20 acceptable castings?", 2310),
    (21, "What would happen if the customer wants to pay $1680 per casting for 20 acceptable castings?", 1680),
    (22, "What would happen if the customer wants to pay $2820 per casting for 20 acceptable castings?", 2820),
    (23, "What would happen if the customer wants to pay $1860 per casting for 20 acceptable castings?", 1860),
    (24, "What would happen if the customer wants to pay $2460 per casting for 20 acceptable castings?", 2460),
    (25, "What would happen if the customer wants to pay $1980 per casting for 20 acceptable castings?", 1980),
    (26, "What would happen if the customer wants to pay $2760 per casting for 20 acceptable castings?", 2760),
    (27, "What would happen if the customer wants to pay $2100 per casting for 20 acceptable castings?", 2100),
    (28, "What would happen if the customer wants to pay $2580 per casting for 20 acceptable castings?", 2580),
    (29, "What would happen if the customer wants to pay $2220 per casting for 20 acceptable castings?", 2220),
    (30, "What would happen if the customer wants to pay $2640 per casting for 20 acceptable castings?", 2640)
]

# 准备结果存储(每个问题9行)
results = []

for problem_num, description, payment in payment_scenarios:
    expected_profits = {}
    
    # 计算每个Q的期望利润（新价格）
    for Q in Q_values:
        expected_profit = 0
        for i, X in enumerate(X_values):
            # 修改后的利润计算函数
            if X < 20:
                revenue = 300 * Q
                cost = 700 * Q
            elif 20 <= X <= 22:
                revenue = 20 * payment + 1500 * (X - 20) + 300 * (Q - X)
                cost = 700 * Q + 500 * X
            else:
                revenue = 20 * payment + 1500 * 2 + 300 * (Q - 22)
                cost = 700 * Q + 500 * 22
                
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
        f"chatgpt: When the customer wants to pay ${payment} per casting for 20 acceptable castings, "
        f"the maximum expected profit is ${max_profit}, which is a {change_type} of ${abs_diff} "
        f"compared to the original value."
    )
    
    deepseek_response = (
        f"deepseek: When the customer wants to pay ${payment} per casting for 20 acceptable castings, "
        f"the maximum expected profit is ${max_profit}, which is a {change_type} of ${abs_diff} "
        f"compared to the original value."
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
df = pd.DataFrame(results, columns=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])
df.to_excel('plan-questions-set2.xlsx', index=False)

print("分析完成，结果已保存至plan-questions-set2.xlsx")