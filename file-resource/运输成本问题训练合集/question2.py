import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus

# Read the existing Excel file
file_path = "question set2.xlsx"
df = pd.read_excel(file_path)

# Market data
markets = {
    "c1": {"demand": 50000, "warehouses": ["w1", "w2"]},
    "c2": {"demand": 100000, "warehouses": ["w1", "w2"]},
    "c3": {"demand": 50000, "warehouses": ["w1", "w2"]},
    "c4": {"demand": 20000, "warehouses": ["w1"]}  # Can only be supplied from w1
}

# Transportation costs
transport_cost = {
    "p1": {"w1": 0, "w2": 5},
    "p2": {"w1": 4, "w2": 2},
    "w1": {"c1": 3, "c2": 4, "c3": 5, "c4": 4},
    "w2": {"c1": 2, "c2": 1, "c3": 2}
}

# Factory capacity
p2_capacity = 60000

def solve_scenario(change_percent, increase=True):
    """Solve a single scenario with the service level constraint"""
    model = LpProblem("Network_Planning_with_Service_Constraint", LpMinimize)
    
    # Calculate adjusted demands
    adjusted_demands = {}
    for market in markets:
        original_demand = markets[market]["demand"]
        if increase:
            adjusted_demand = original_demand * (1 + change_percent / 100)
        else:
            adjusted_demand = original_demand * (1 - change_percent / 100)
        adjusted_demands[market] = adjusted_demand
    
    # Decision variables
    # Production variables: from plants to warehouses
    x_p1_w1 = LpVariable("x_p1_w1", lowBound=0)
    x_p1_w2 = LpVariable("x_p1_w2", lowBound=0)
    x_p2_w1 = LpVariable("x_p2_w1", lowBound=0)
    x_p2_w2 = LpVariable("x_p2_w2", lowBound=0)
    
    # Distribution variables: from warehouses to markets
    y_w1_c1 = LpVariable("y_w1_c1", lowBound=0)
    y_w1_c2 = LpVariable("y_w1_c2", lowBound=0)
    y_w1_c3 = LpVariable("y_w1_c3", lowBound=0)
    y_w1_c4 = LpVariable("y_w1_c4", lowBound=0)
    y_w2_c1 = LpVariable("y_w2_c1", lowBound=0)
    y_w2_c2 = LpVariable("y_w2_c2", lowBound=0)
    y_w2_c3 = LpVariable("y_w2_c3", lowBound=0)
    
    # Binary variables to select which market to under-serve
    y1 = LpVariable("y1", cat='Binary')  # Under-serve c1
    y2 = LpVariable("y2", cat='Binary')  # Under-serve c2
    y3 = LpVariable("y3", cat='Binary')  # Under-serve c3
    y4 = LpVariable("y4", cat='Binary')  # Under-serve c4
    
    # Objective function (minimize total cost)
    model += (
        0 * x_p1_w1 + 5 * x_p1_w2 + 4 * x_p2_w1 + 2 * x_p2_w2 +
        3 * y_w1_c1 + 4 * y_w1_c2 + 5 * y_w1_c3 + 4 * y_w1_c4 +
        2 * y_w2_c1 + 1 * y_w2_c2 + 2 * y_w2_c3
    )
    
    # Constraints
    # Plant capacity constraint
    model += x_p2_w1 + x_p2_w2 <= p2_capacity
    
    # Warehouse balance constraints
    model += x_p1_w1 + x_p2_w1 == y_w1_c1 + y_w1_c2 + y_w1_c3 + y_w1_c4
    model += x_p1_w2 + x_p2_w2 == y_w2_c1 + y_w2_c2 + y_w2_c3
    
    # Market demand constraints with under-serving
    model += y_w1_c1 + y_w2_c1 >= adjusted_demands["c1"] * (0.8 + 0.2 * (1 - y1))
    model += y_w1_c2 + y_w2_c2 >= adjusted_demands["c2"] * (0.8 + 0.2 * (1 - y2))
    model += y_w1_c3 + y_w2_c3 >= adjusted_demands["c3"] * (0.8 + 0.2 * (1 - y3))
    model += y_w1_c4 >= adjusted_demands["c4"] * (0.8 + 0.2 * (1 - y4))
    
    # Only one market can be under-served
    model += y1 + y2 + y3 + y4 == 1
    
    # Solve the problem
    model.solve()
    
    if model.status == 1:
        result = {
            "adjusted_demands": adjusted_demands,
            "total_cost": model.objective.value(),
            "variables": {
                "x_p1_w1": x_p1_w1.value(),
                "x_p1_w2": x_p1_w2.value(),
                "x_p2_w1": x_p2_w1.value(),
                "x_p2_w2": x_p2_w2.value(),
                "y_w1_c1": y_w1_c1.value(),
                "y_w1_c2": y_w1_c2.value(),
                "y_w1_c3": y_w1_c3.value(),
                "y_w1_c4": y_w1_c4.value(),
                "y_w2_c1": y_w2_c1.value(),
                "y_w2_c2": y_w2_c2.value(),
                "y_w2_c3": y_w2_c3.value(),
                "y1": y1.value(),
                "y2": y2.value(),
                "y3": y3.value(),
                "y4": y4.value()
            }
        }
        return result
    else:
        return None

# Fixed 30 problem scenarios
scenarios = [
    {"Problem Number": 1, "change_percent": 23, "increase": True},
    {"Problem Number": 2, "change_percent": 45, "increase": False},
    {"Problem Number": 3, "change_percent": 67, "increase": True},
    {"Problem Number": 4, "change_percent": 18, "increase": False},
    {"Problem Number": 5, "change_percent": 89, "increase": True},
    {"Problem Number": 6, "change_percent": 31, "increase": False},
    {"Problem Number": 7, "change_percent": 52, "increase": True},
    {"Problem Number": 8, "change_percent": 76, "increase": False},
    {"Problem Number": 9, "change_percent": 14, "increase": True},
    {"Problem Number": 10, "change_percent": 97, "increase": False},
    {"Problem Number": 11, "change_percent": 38, "increase": True},
    {"Problem Number": 12, "change_percent": 55, "increase": False},
    {"Problem Number": 13, "change_percent": 72, "increase": True},
    {"Problem Number": 14, "change_percent": 29, "increase": False},
    {"Problem Number": 15, "change_percent": 63, "increase": True},
    {"Problem Number": 16, "change_percent": 41, "increase": False},
    {"Problem Number": 17, "change_percent": 85, "increase": True},
    {"Problem Number": 18, "change_percent": 12, "increase": False},
    {"Problem Number": 19, "change_percent": 34, "increase": True},
    {"Problem Number": 20, "change_percent": 58, "increase": False},
    {"Problem Number": 21, "change_percent": 91, "increase": True},
    {"Problem Number": 22, "change_percent": 27, "increase": False},
    {"Problem Number": 23, "change_percent": 46, "increase": True},
    {"Problem Number": 24, "change_percent": 79, "increase": False},
    {"Problem Number": 25, "change_percent": 15, "increase": True},
    {"Problem Number": 26, "change_percent": 64, "increase": False},
    {"Problem Number": 27, "change_percent": 37, "increase": True},
    {"Problem Number": 28, "change_percent": 82, "increase": False},
    {"Problem Number": 29, "change_percent": 53, "increase": True},
    {"Problem Number": 30, "change_percent": 96, "increase": False}
]

# Solve all scenarios and update DataFrame
for scenario in scenarios:
    prob_num = scenario["Problem Number"]
    change_percent = scenario["change_percent"]
    increase = scenario["increase"]
    
    result = solve_scenario(change_percent, increase)
    
    if result:
        # Determine which market is under-served
        under_served = None
        if result["variables"]["y1"] == 1:
            under_served = "c1"
        elif result["variables"]["y2"] == 1:
            under_served = "c2"
        elif result["variables"]["y3"] == 1:
            under_served = "c3"
        elif result["variables"]["y4"] == 1:
            under_served = "c4"
        
        # Prepare demand description
        demand_desc = (
            f"The demand for c1, c2, c3, and c4 markets has respectively become "
            f"[{result['adjusted_demands']['c1']:.0f}, {result['adjusted_demands']['c2']:.0f}, "
            f"{result['adjusted_demands']['c3']:.0f}, {result['adjusted_demands']['c4']:.0f}]. "
            f"Market {under_served} is under-served at 80% of its demand."
        )
        
        # ChatGPT response format
        chatgpt_response = (
            f"{demand_desc} Therefore, the final optimal plan is as follows:\n"
            f"x_p1_w1: {result['variables']['x_p1_w1']:.0f}\n"
            f"x_p1_w2: {result['variables']['x_p1_w2']:.0f}\n"
            f"x_p2_w1: {result['variables']['x_p2_w1']:.0f}\n"
            f"x_p2_w2: {result['variables']['x_p2_w2']:.0f}\n"
            f"y_w1_c1: {result['variables']['y_w1_c1']:.0f}\n"
            f"y_w1_c2: {result['variables']['y_w1_c2']:.0f}\n"
            f"y_w1_c3: {result['variables']['y_w1_c3']:.0f}\n"
            f"y_w1_c4: {result['variables']['y_w1_c4']:.0f}\n"
            f"y_w2_c1: {result['variables']['y_w2_c1']:.0f}\n"
            f"y_w2_c2: {result['variables']['y_w2_c2']:.0f}\n"
            f"y_w2_c3: {result['variables']['y_w2_c3']:.0f}\n"
            f"And the total cost is {result['total_cost']:.2f}\n"
            f"(请chatgpt将final optimal plan以表的形式展示，纵坐标是'w1,w2' 横坐标是'P1 P2 C1 C2 C3 C4')"
        )
        
        # DeepSeek response format
        deepseek_response = (
            f"{demand_desc} Therefore, the final optimal plan is as follows:\n"
            f"x_p1_w1: {result['variables']['x_p1_w1']:.0f}\n"
            f"x_p1_w2: {result['variables']['x_p1_w2']:.0f}\n"
            f"x_p2_w1: {result['variables']['x_p2_w1']:.0f}\n"
            f"x_p2_w2: {result['variables']['x_p2_w2']:.0f}\n"
            f"y_w1_c1: {result['variables']['y_w1_c1']:.0f}\n"
            f"y_w1_c2: {result['variables']['y_w1_c2']:.0f}\n"
            f"y_w1_c3: {result['variables']['y_w1_c3']:.0f}\n"
            f"y_w1_c4: {result['variables']['y_w1_c4']:.0f}\n"
            f"y_w2_c1: {result['variables']['y_w2_c1']:.0f}\n"
            f"y_w2_c2: {result['variables']['y_w2_c2']:.0f}\n"
            f"y_w2_c3: {result['variables']['y_w2_c3']:.0f}\n"
            f"And the total cost is {result['total_cost']:.2f}\n"
            f"(请deepseek将final optimal plan以表的形式展示，纵坐标是'w1,w2' 横坐标是'P1 P2 C1 C2 C3 C4')"
        )
        
        # Update DataFrame
        df.loc[df["Problem Number"] == prob_num, "ChatGPT Response"] = chatgpt_response
        df.loc[df["Problem Number"] == prob_num, "DeepSeek Response"] = deepseek_response

# Save the updated Excel file
df.to_excel(file_path, index=False)
print("Results have been successfully written to the Excel file.")