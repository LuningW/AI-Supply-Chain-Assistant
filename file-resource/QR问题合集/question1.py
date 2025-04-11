import pandas as pd
import math

# Given constants
K = 900  # fixed ordering cost ($/order)
h = 20   # monthly holding cost ($/table/month) (240/12)

# List of demand values (200-500, excluding 360, randomized order)
demand_values = [470, 230, 390, 310, 450, 280, 340, 500, 210, 370, 
                 440, 260, 330, 490, 240, 410, 300, 480, 220, 350, 
                 430, 290, 400, 250, 460, 320, 380, 200, 420, 270]

# Function to calculate EOQ
def calculate_eoq(D):
    return math.sqrt((2 * K * D) / h)

# Prepare data for Excel
data = []
problem_number = 1

for D in demand_values:
    Q = round(calculate_eoq(D))
    
    scenario_desc = f"What is the order quantity Q per month if the average monthly demand becomes {D} tables?"
    
    chatgpt_response = f"chatgpt: When the average monthly demand becomes {D} tables, the order quantity Q per month is {Q} tables."
    deepseek_response = f"deepseek: When the average monthly demand becomes {D} tables, the order quantity Q per month is {Q} tables."
    
    # Add 9 identical rows for each problem
    for _ in range(9):
        data.append([
            problem_number,
            scenario_desc,
            chatgpt_response,  # 现在第三列是ChatGPT
            deepseek_response  # 第四列是DeepSeek
        ])
    
    problem_number += 1

# Create DataFrame - 注意列顺序已调整
df = pd.DataFrame(data, columns=[
    "Problem Number",
    "Scenario Description",
    "ChatGPT Response",  # 第三列
    "DeepSeek Response"  # 第四列
])

# Save to Excel
df.to_excel("plan-questions-set1.xlsx", index=False)

print("Excel file 'plan-questions-set1.xlsx' has been created successfully with adjusted column order.")