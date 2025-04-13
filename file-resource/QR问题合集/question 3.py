import pandas as pd
import random

# Expression templates with placeholder {stock_term} for safety stock synonyms
templates = [
    # Question forms
    "Given a standard deviation of {std_dev} tables and {service_level}% service level, what's the required {stock_term}?",
    "How much {stock_term} is needed when σ={std_dev} tables at {service_level}% service level?",
    "What {stock_term} (rounded down) is appropriate for σ={std_dev} and {service_level}% service?",
    "Can you calculate the {stock_term} needed for σ={std_dev} tables with {service_level}% service?",
    "At {service_level}% service level and σ={std_dev} tables, what should our {stock_term} be?",
    "For inventory with σ={std_dev} tables, what's the {service_level}% service level {stock_term}?",
    "What's the floor value of {stock_term} when σ={std_dev} and service level is {service_level}%?",
    "How do we determine the {stock_term} when standard deviation is {std_dev} at {service_level}% service?",
    "Could you compute the {stock_term} required for σ={std_dev} tables and {service_level}% service?",
    "What's the exact {stock_term} needed when σ={std_dev} with {service_level}% service level?",
    
    # Statement forms
    "Calculate the {stock_term} given σ={std_dev} tables and {service_level}% service level.",
    "Determine the {stock_term} needed for standard deviation of {std_dev} tables at {service_level}% service.",
    "We need to find the {stock_term} when σ={std_dev} with {service_level}% service level.",
    "Compute the appropriate {stock_term} for σ={std_dev} tables and {service_level}% service.",
    "The {stock_term} must be calculated for σ={std_dev} at {service_level}% service level.",
    "Find the floor value of {stock_term} when standard deviation is {std_dev} and service level is {service_level}%.",
    "Establish the required {stock_term} given σ={std_dev} tables and {service_level}% service.",
    "Derive the {stock_term} amount needed for σ={std_dev} at {service_level}% service level.",
    "Figure out the {stock_term} when standard deviation is {std_dev} tables with {service_level}% service.",
    "The {service_level}% service level {stock_term} needs to be determined for σ={std_dev} tables."
]

SAFETY_STOCK_SYNONYMS = [
    "safety stock",
    "buffer inventory",
    "minimum stock level",
    "protection inventory",
    "emergency reserve"
]

def generate_variations(original_question):
    # Extract parameters
    std_dev = int(original_question.split("is ")[1].split(" tables")[0])
    service_level = int(original_question.split("of ")[1].split("%")[0])
    
    variations = []
    selected_templates = random.sample(templates, 8)
    
    for template in selected_templates:
        # Randomly select a synonym for each variation
        stock_term = random.choice(SAFETY_STOCK_SYNONYMS)
        variation = template.format(
            std_dev=std_dev,
            service_level=service_level,
            stock_term=stock_term
        )
        variations.append(variation)
    
    return [original_question] + variations

def process_file(input_file, output_file):
    df = pd.read_excel(input_file)
    new_rows = []
    
    for i in range(0, len(df), 9):
        original_row = df.iloc[i]
        original_question = original_row['Scenario Description']
        
        variations = generate_variations(original_question)
        
        for j in range(9):
            new_row = original_row.copy()
            new_row['Scenario Description'] = variations[j] if j < len(variations) else variations[-1]
            new_rows.append(new_row)
    
    new_df = pd.DataFrame(new_rows)
    new_df.to_excel(output_file, index=False)
    print(f"Modified file with synonyms saved as {output_file}")

# Process the file
process_file("questions set2.xlsx", "plan-questions-set2.xlsx")
