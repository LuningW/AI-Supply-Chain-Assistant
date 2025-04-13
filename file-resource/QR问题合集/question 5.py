import pandas as pd
import math

# Parameters
mu = 360       # Average monthly demand
sigma = 45     # Standard deviation
z = 1.65       # Z-score for 95% service level
L = 0.5        # Lead time in months

# Review periods from the 30 generated questions
r_values = [
    7.4, 2.6, 9.2, 3.8, 5.8, 1.4, 6.2, 8.0, 4.4, 10.0,
    2.0, 6.6, 9.6, 5.2, 8.8, 3.2, 7.8, 1.8, 4.8, 6.4,
    2.8, 9.0, 5.6, 7.2, 8.4, 3.6, 4.2, 1.6, 8.6, 9.8
]

data = []

for problem_num, r in enumerate(r_values, 1):
    # Calculate base-stock level
    total_period = r + L
    mean_demand = mu * total_period
    safety_stock = z * sigma * math.sqrt(total_period)
    base_stock = mean_demand + safety_stock
    
    # Truncate to integer and keep original value with two decimals
    truncated = int(base_stock)
    original = round(base_stock, 2)
    
    # Scenario description
    scenario = f"The store plan to adopt periodic review policy with a review period r of {r} month. What is the base-stock level per month?"
    
    # Format responses
    chatgpt_resp = f"chatgpt: After adopting the periodic review policy and r= {r} month, the base-stock level per month is {truncated} (originally calculated as {original:.2f}) tables."
    deepseek_resp = f"deepseek: After adopting the periodic review policy and r= {r} month, the base-stock level per month is {truncated} (originally calculated as {original:.2f}) tables."
    
    # Add 9 entries per problem
    for _ in range(9):
        data.append({
            "Problem Number": problem_num,
            "Scenario Description": scenario,
            "ChatGPT Response": chatgpt_resp,
            "DeepSeek Response": deepseek_resp
        })

# Create DataFrame and save to Excel
df = pd.DataFrame(data)
df.to_excel("plan-questions-set5.xlsx", index=False, 
            columns=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])
