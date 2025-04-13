import pandas as pd
import numpy as np
import math
import random

# Given parameters
z = 1.65
L = 0.5

# Sample sentence templates (20 total)
templates = [
    # Question-style (10)
    "Given a mean demand of {μ} units and variability of {σ} units, what should the reorder point be?",
    "How do we determine the restocking threshold when monthly sales average {μ} with {σ} standard deviation?",
    "What's the optimal inventory trigger point for demand N({μ},{σ}²)?",
    "At what stock level should we reorder given μ={μ} and σ={σ}?",
    "Can you compute the replenishment point for demand parameters {μ} (avg) and {σ} (stdev)?",
    "Where should we set the reorder marker when demand has mean {μ} and std dev {σ}?",
    "What inventory level warrants new orders with demand characteristics {μ}±{σ}?",
    "How to calculate the order trigger when typical demand is {μ} with {σ} fluctuation?",
    "What's the suggested reorder quantity given demand distribution N({μ},{σ}²)?",
    "When should we place orders if product demand follows N({μ},{σ}²)?",
    
    # Statement-style (10)
    "Compute the reorder level for demand averaging {μ} units with {σ} unit standard deviation.",
    "Determine the stock replenishment point given demand mean {μ} and stdev {σ}.",
    "Find the inventory threshold that triggers ordering for demand N({μ},{σ}²).",
    "Establish the reorder quantity when demand has mean {μ} and variance {σ}².",
    "Calculate the order point for normally distributed demand with μ={μ}, σ={σ}.",
    "Identify the restocking level appropriate for demand parameters {μ} (mean) and {σ} (stdev).",
    "Specify the inventory level that initiates reorders given demand N({μ},{σ}²).",
    "Assess the reorder threshold needed for demand characteristics {μ}±{σ}.",
    "Figure out when to reorder stock with demand distribution N({μ},{σ}²).",
    "Set the replenishment trigger point for demand averaging {μ} with {σ} standard deviation."
]

# Problems data
problems = [
    (427, 28), (312, 9), (485, 15), (203, 37), (376, 4),
    (291, 22), (498, 19), (224, 31), (359, 11), (411, 26),
    (267, 40), (342, 7), (478, 13), (215, 34), (396, 2),
    (303, 24), (452, 17), (239, 29), (387, 8), (421, 21),
    (254, 38), (365, 5), (492, 12), (208, 35), (334, 3),
    (279, 25), (463, 16), (228, 30), (401, 10), (436, 20)
]

# Function to calculate reorder level
def calculate_reorder_level(μ, σ):
    original_R = μ * L + z * σ * np.sqrt(L)
    return int(original_R), original_R

# Prepare data
data = []
for i, (μ, σ) in enumerate(problems, 1):
    integer_R, original_R = calculate_reorder_level(μ, σ)
    original_question = f"What is the reorder level R for this store per month with an average {μ} tables and a standard deviation {σ} tables"
    
    # Keep first line as original question
    data.append({
        "Problem Number": i,
        "Scenario Description": original_question,
        "ChatGPT Response": f"chatgpt: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables.",
        "DeepSeek Response": f"deepseek: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables."
    })
    
    # Select 8 random templates
    selected_templates = random.sample(templates, 8)
    
    # Add 8 variations
    for template in selected_templates:
        varied_question = template.format(μ=μ, σ=σ)
        data.append({
            "Problem Number": i,
            "Scenario Description": varied_question,
            "ChatGPT Response": f"chatgpt: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables.",
            "DeepSeek Response": f"deepseek: When μ = {μ} tables and σ = {σ}, the reorder level R for this store per month is {integer_R} (originally calculated as {original_R:.2f}) tables."
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save to Excel
with pd.ExcelWriter("plan-questions-set4-modified.xlsx", engine='openpyxl') as writer:
    df.to_excel(writer, index=False, header=["Problem Number", "Scenario Description", "ChatGPT Response", "DeepSeek Response"])

print("Modified Excel file 'plan-questions-set4-modified.xlsx' created successfully.")