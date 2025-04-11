from pulp import LpMinimize, LpProblem, LpVariable, lpSum
import random
import pandas as pd

markets = ["c1", "c2", "c3", "c4"]
initial_demands = {"c1": 50000, "c2": 100000, "c3": 50000, "c4": 20000}
factory_capacity = 60000

scenarios = []
for _ in range(30):
    market = random.choice(markets)
    percent = random.randint(5, 30)
    scenarios.append((market, percent))

# 创建足够大的DataFrame (30情景×8行间隔=240行，加上第241行)
total_rows = 1 + (30 * 8)  # 第1行开始，每8行一个情景，共30个情景
df = pd.DataFrame(index=range(total_rows), columns=[
    "Problem Number", 
    "Scenario Description", 
    "ChatGPT Response", 
    "DeepSeek Response"
])

for i, (target_market, increase_pct) in enumerate(scenarios, 1):
    adjusted_demands = initial_demands.copy()
    adjusted_demands[target_market] = int(initial_demands[target_market] * (1 + increase_pct/100))
    
    model = LpProblem(f"Scenario_{i}", LpMinimize)
    
    # 变量和模型设置
    x = {}
    for src in ["p1", "p2"]:
        for dst in ["w1", "w2"]:
            x[f"x_{src}_{dst}"] = LpVariable(f"x_{src}_{dst}", lowBound=0)
    for src in ["w1", "w2"]:
        for dst in markets:
            if src == "w2" and dst == "c4":
                continue
            x[f"x_{src}_{dst}"] = LpVariable(f"x_{src}_{dst}", lowBound=0)
    
    y = {f"y_{m}": LpVariable(f"y_{m}", cat='Binary') for m in markets}
    
    demand_adjustments = {"c1": 10000, "c2": 20000, "c3": 10000, "c4": 4000}
    d = {m: adjusted_demands[m] - y[f"y_{m}"] * demand_adjustments[m] for m in markets}
    
    transport_cost = (
        0*x["x_p1_w1"] + 5*x["x_p1_w2"] +
        4*x["x_p2_w1"] + 2*x["x_p2_w2"] +
        3*x["x_w1_c1"] + 4*x["x_w1_c2"] + 5*x["x_w1_c3"] + 4*x["x_w1_c4"] +
        2*x["x_w2_c1"] + 1*x["x_w2_c2"] + 2*x["x_w2_c3"]
    )
    model += transport_cost
    
    model += x["x_p2_w1"] + x["x_p2_w2"] <= factory_capacity
    
    model += x["x_p1_w1"] + x["x_p2_w1"] == lpSum([x[f"x_w1_{m}"] for m in markets])
    model += x["x_p1_w2"] + x["x_p2_w2"] == lpSum([x[f"x_w2_{m}"] for m in markets if m != "c4"])
    
    model += x["x_w1_c1"] + x["x_w2_c1"] == d["c1"]
    model += x["x_w1_c2"] + x["x_w2_c2"] == d["c2"]
    model += x["x_w1_c3"] + x["x_w2_c3"] == d["c3"]
    model += x["x_w1_c4"] == d["c4"]
    
    model += lpSum(y.values()) == 1
    
    status = model.solve()
    
    reduced_market = next(m for m in markets if y[f"y_{m}"].varValue > 0.9)
    transport_plan = "\n".join([f"{var}: {x[var].varValue:.0f}" for var in sorted(x) if x[var].varValue > 1e-6])
    
    # 准备输出内容
    row_index = (i-1)*8  # 第1个情景在第0行，第2个在第8行，...，第30个在第232行(Excel中第233行)
    
    scenario_desc = f"What would happen if the demand at market {target_market} increased by {increase_pct}%"
    
    chatgpt_response = (
        f"the demand at market {target_market} has become {adjusted_demands[target_market]}. "
        f"So the optimal solution has also changed: {transport_plan}. "
        f"And the total cost is ${model.objective.value():.2f}"
    )
    
    deepseek_response = (
        f"the demand at market {target_market} has become {adjusted_demands[target_market]}. "
        f"So the optimal solution has also changed: demand at {reduced_market} was reduced by {demand_adjustments[reduced_market]}. "
        f"And the total cost is ${model.objective.value():.2f}"
    )
    
    # 填充DataFrame
    df.at[row_index, "Problem Number"] = i
    df.at[row_index, "Scenario Description"] = scenario_desc
    df.at[row_index, "ChatGPT Response"] = f"user: {scenario_desc}\nchatgpt: {chatgpt_response}"
    df.at[row_index, "DeepSeek Response"] = f"user: {scenario_desc}\ndeepseek: {deepseek_response}"

# 保存到Excel
df.to_excel("supply_chain_scenarios_spaced.xlsx", index=False)
print(f"结果已保存到 supply_chain_scenarios_spaced.xlsx，共{total_rows}行")