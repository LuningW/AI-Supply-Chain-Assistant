import pandas as pd
import numpy as np
import math

# Given parameters
μ = 360  # average monthly demand (tables)
σ = 45   # standard deviation of monthly demand
z = 1.65 # z-score for 95% service level

# List of lead times (0.1 to 4.0 in 0.1 increments, randomly ordered)
lead_times = [1.7, 0.3, 2.4, 0.8, 3.1, 1.2, 0.5, 2.9, 0.1, 3.6,
              1.5, 0.7, 2.1, 0.4, 3.9, 1.9, 0.6, 2.7, 0.2, 3.3,
              1.0, 0.9, 2.5, 3.8, 1.4, 4.0, 2.0, 1.8, 3.5, 2.3]

# Function to calculate reorder level R (truncate decimals)
def calculate_reorder_level(L):
    original_R = μ * L + z * σ * np.sqrt(L)
    integer_R = int(math.floor(original_R))
    return integer_R, original_R

# Prepare data for DataFrame
data = []
problem_number = 1

for L in lead_times:
    integer_R, original_R = calculate_reorder_level(L)
    scenario_desc = f"What is the reorder level R for this store per month that the lead time equal to {L} month?"
    
    chatgpt_response = f"chatgpt: When the lead time is {L} month, the reorder level R for this store per month is {integer_R}(originally calculated as {original_R:.2f}) tables."
    deepseek_response = f"deepseek: When the lead time is {L} month, the reorder level R for this store per month is {integer_R}(originally calculated as {original_R:.2f}) tables."
    
    # Repeat each problem 9 times
    for _ in range(9):
        data.append({
            "Problem Number": problem_number,
            "Scenario Description": scenario_desc,
            "ChatGPT Response": chatgpt_response,
            "DeepSeek Response": deepseek_response
        })
    
    problem_number += 1

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
with pd.ExcelWriter("plan-questions-set3.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, index=False, header=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])

print("Excel file 'plan-questions-set3.xlsx' has been created successfully.")