import pandas as pd
import numpy as np

# Define all 30 scenarios
scenarios = [
    (17, "What would happen if the order becomes 17 custom-designed castings..."),
    (33, "What would happen if the order becomes 33 custom-designed castings..."),
    (12, "What would happen if the order becomes 12 custom-designed castings..."),
    (41, "What would happen if the order becomes 41 custom-designed castings..."),
    (25, "What would happen if the order becomes 25 custom-designed castings..."),
    (29, "What would happen if the order becomes 29 custom-designed castings..."),
    (15, "What would happen if the order becomes 15 custom-designed castings..."),
    (37, "What would happen if the order becomes 37 custom-designed castings..."),
    (22, "What would happen if the order becomes 22 custom-designed castings..."),
    (31, "What would happen if the order becomes 31 custom-designed castings..."),
    (13, "What would happen if the order becomes 13 custom-designed castings..."),
    (38, "What would happen if the order becomes 38 custom-designed castings..."),
    (19, "What would happen if the order becomes 19 custom-designed castings..."),
    (27, "What would happen if the order becomes 27 custom-designed castings..."),
    (34, "What would happen if the order becomes 34 custom-designed castings..."),
    (11, "What would happen if the order becomes 11 custom-designed castings..."),
    (42, "What would happen if the order becomes 42 custom-designed castings..."),
    (23, "What would happen if the order becomes 23 custom-designed castings..."),
    (16, "What would happen if the order becomes 16 custom-designed castings..."),
    (36, "What would happen if the order becomes 36 custom-designed castings..."),
    (14, "What would happen if the order becomes 14 custom-designed castings..."),
    (39, "What would happen if the order becomes 39 custom-designed castings..."),
    (26, "What would happen if the order becomes 26 custom-designed castings..."),
    (32, "What would happen if the order becomes 32 custom-designed castings..."),
    (18, "What would happen if the order becomes 18 custom-designed castings..."),
    (35, "What would happen if the order becomes 35 custom-designed castings..."),
    (24, "What would happen if the order becomes 24 custom-designed castings..."),
    (30, "What would happen if the order becomes 30 custom-designed castings..."),
    (21, "What would happen if the order becomes 21 custom-designed castings..."),
    (28, "What would happen if the order becomes 28 custom-designed castings...")
]


# Prepare expanded results storage (9 rows per problem)
expanded_results = []

# Process each scenario
for problem_num, (value, description) in enumerate(scenarios, 1):
    # Read Excel file
    file_path = 'C:/Users/huyyehg/Desktop/5401 project/生产计划问题/训练数据.xlsx'
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    
    # Extract Q and X values
    Q_values = [int(col.split('=')[1]) for col in data.columns[1:]]
    X_values = [int(row.split('=')[1]) for row in data['Unnamed: 0']]
    probabilities = data.iloc[:, 1:].values
    
    # Profit calculation function
    def calculate_profit(Q, X, value):
        if X < value:
            revenue = 300 * Q
            cost = 700 * Q
        elif value <= X <= value+2:
            revenue = value * 2000 + 1500 * (X - value) + 300 * (Q - X)
            cost = 700 * Q + 500 * X
        else:
            revenue = value * 2000 + 1500 * 2 + 300 * (Q - (value+2))
            cost = 700 * Q + 500 * (value+2)
        return revenue - cost
    
    # Calculate metrics
    expected_profits = {}
    loss_probabilities = {}
    
    for Q in Q_values:
        expected_profit = 0
        loss_prob = 0
        for i, X in enumerate(X_values):
            profit = calculate_profit(Q, X, value)
            prob = probabilities[i, Q_values.index(Q)]
            expected_profit += profit * prob
            if profit < 0:
                loss_prob += prob
        expected_profits[Q] = round(expected_profit, 2)
        loss_probabilities[Q] = round(loss_prob, 4)
    
    # Find optimal solution
    optimal_Q = max(expected_profits, key=expected_profits.get)
    max_profit = expected_profits[optimal_Q]
    optimal_loss_prob = loss_probabilities[optimal_Q]
    
    # Format responses
    chatgpt_response = (f"chatgpt: When the order is {value} units, the optimal number of casting scheduled "
                       f"is {optimal_Q} units with an expected profit of {max_profit}. And its "
                       f"probability of losing money is {optimal_loss_prob}")
    
    deepseek_response = (f"deepseek: When the order is {value} units, the optimal production quantity "
                        f"is {optimal_Q} units, yielding an expected profit of {max_profit} with "
                        f"a {optimal_loss_prob} risk of loss.")
    
    # Create 9 identical rows for this problem
    for _ in range(9):
        expanded_results.append({
            "Problem Number": problem_num,
            "Scenario Description": description,
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# Create DataFrame with exact column order
columns_order = ["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"]
df = pd.DataFrame(expanded_results, columns=columns_order)

# Save to Excel with no index and exact header
output_path = 'plan-questions-set1.xlsx'
df.to_excel(output_path, index=False, header=True)

print(f"File saved to {output_path}")
print(f"Total rows: {len(df)} (30 problems × 9 rows each)")