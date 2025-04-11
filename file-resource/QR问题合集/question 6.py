import pandas as pd
import numpy as np
import math

# Given parameters
z = 1.65  # z-score for 95% service level
L = 0.5   # lead time in months (fixed as per original conditions)

# Problems data (from previous generation)
problems = [
    (427, 28), (312, 9), (485, 15), (203, 37), (376, 4),
    (291, 22), (498, 19), (224, 31), (359, 11), (411, 26),
    (267, 40), (342, 7), (478, 13), (215, 34), (396, 2),
    (303, 24), (452, 17), (239, 29), (387, 8), (421, 21),
    (254, 38), (365, 5), (492, 12), (208, 35), (334, 3),
    (279, 25), (463, 16), (228, 30), (401, 10), (436, 20)
]

# Function to calculate reorder level (truncate decimals)
def calculate_reorder_level(μ, σ):
    original_R = μ * L + z * σ * np.sqrt(L)
    integer_R = int(math.floor(original_R))
    return integer_R, original_R

# Prepare data for DataFrame
data = []
for i, (μ, σ) in enumerate(problems, 1):
    integer_R, original_R = calculate_reorder_level(μ, σ)
    scenario_desc = f"What is the reorder level R for this store per month with an average {μ} tables and a standard deviation {σ} tables"
    
    chatgpt_response = f"chatgpt: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables."
    deepseek_response = f"deepseek: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables."
    
    # First row - original question
    data.append({
        "Problem Number": i,
        "Scenario Description": scenario_desc,
        "ChatGPT Response": chatgpt_response,
        "DeepSeek Response": deepseek_response
    })
    
    # Next 8 rows - same answers (repeated)
    for _ in range(8):
        data.append({
            "Problem Number": i,
            "Scenario Description": scenario_desc,
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
with pd.ExcelWriter("plan-questions-set4.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, index=False, header=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])

print("Excel file 'plan-questions-set4.xlsx' has been created successfully.")