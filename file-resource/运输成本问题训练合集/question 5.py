import pandas as pd
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus

# 加载现有Excel文件
file_path = "question set5.xlsx"
df = pd.read_excel(file_path)

# 原始问题数据
markets = {
    "c1": {"demand": 50000, "warehouses": ["w1", "w2"]},
    "c2": {"demand": 100000, "warehouses": ["w1", "w2"]},
    "c3": {"demand": 50000, "warehouses": ["w1", "w2"]},
    "c4": {"demand": 20000, "warehouses": ["w1"]}
}

transport_cost = {
    "p1": {"w1": 0, "w2": 5},
    "p2": {"w1": 4, "w2": 2},
    "w1": {"c1": 3, "c2": 4, "c3": 5, "c4": 4},
    "w2": {"c1": 2, "c2": 1, "c3": 2}
}

original_p2_capacity = 60000

# 30个固定场景
scenarios = [
    {"Problem Number": 1, "type": "decrease", "percent": 37, "new_capacity": original_p2_capacity * 0.37},
    {"Problem Number": 2, "type": "increase", "percent": 68, "new_capacity": original_p2_capacity * 1.68},
    {"Problem Number": 3, "type": "decrease", "percent": 83, "new_capacity": original_p2_capacity * 0.83},
    {"Problem Number": 4, "type": "increase", "percent": 15, "new_capacity": original_p2_capacity * 1.15},
    {"Problem Number": 5, "type": "decrease", "percent": 52, "new_capacity": original_p2_capacity * 0.52},
    {"Problem Number": 6, "type": "increase", "percent": 91, "new_capacity": original_p2_capacity * 1.91},
    {"Problem Number": 7, "type": "decrease", "percent": 24, "new_capacity": original_p2_capacity * 0.24},
    {"Problem Number": 8, "type": "increase", "percent": 76, "new_capacity": original_p2_capacity * 1.76},
    {"Problem Number": 9, "type": "decrease", "percent": 65, "new_capacity": original_p2_capacity * 0.65},
    {"Problem Number": 10, "type": "increase", "percent": 29, "new_capacity": original_p2_capacity * 1.29},
    {"Problem Number": 11, "type": "decrease", "percent": 18, "new_capacity": original_p2_capacity * 0.18},
    {"Problem Number": 12, "type": "increase", "percent": 47, "new_capacity": original_p2_capacity * 1.47},
    {"Problem Number": 13, "type": "decrease", "percent": 72, "new_capacity": original_p2_capacity * 0.72},
    {"Problem Number": 14, "type": "increase", "percent": 33, "new_capacity": original_p2_capacity * 1.33},
    {"Problem Number": 15, "type": "decrease", "percent": 41, "new_capacity": original_p2_capacity * 0.41},
    {"Problem Number": 16, "type": "increase", "percent": 88, "new_capacity": original_p2_capacity * 1.88},
    {"Problem Number": 17, "type": "decrease", "percent": 56, "new_capacity": original_p2_capacity * 0.56},
    {"Problem Number": 18, "type": "increase", "percent": 12, "new_capacity": original_p2_capacity * 1.12},
    {"Problem Number": 19, "type": "decrease", "percent": 94, "new_capacity": original_p2_capacity * 0.94},
    {"Problem Number": 20, "type": "increase", "percent": 61, "new_capacity": original_p2_capacity * 1.61},
    {"Problem Number": 21, "type": "decrease", "percent": 27, "new_capacity": original_p2_capacity * 0.27},
    {"Problem Number": 22, "type": "increase", "percent": 79, "new_capacity": original_p2_capacity * 1.79},
    {"Problem Number": 23, "type": "decrease", "percent": 49, "new_capacity": original_p2_capacity * 0.49},
    {"Problem Number": 24, "type": "increase", "percent": 23, "new_capacity": original_p2_capacity * 1.23},
    {"Problem Number": 25, "type": "decrease", "percent": 85, "new_capacity": original_p2_capacity * 0.85},
    {"Problem Number": 26, "type": "increase", "percent": 54, "new_capacity": original_p2_capacity * 1.54},
    {"Problem Number": 27, "type": "decrease", "percent": 31, "new_capacity": original_p2_capacity * 0.31},
    {"Problem Number": 28, "type": "increase", "percent": 97, "new_capacity": original_p2_capacity * 1.97},
    {"Problem Number": 29, "type": "decrease", "percent": 63, "new_capacity": original_p2_capacity * 0.63},
    {"Problem Number": 30, "type": "increase", "percent": 42, "new_capacity": original_p2_capacity * 1.42}
]

def solve_scenario(p2_capacity):
    """求解运输问题"""
    model = LpProblem("Network_Planning", LpMinimize)
    
    # 决策变量
    x_p1_w1 = LpVariable("x_p1_w1", lowBound=0)
    x_p1_w2 = LpVariable("x_p1_w2", lowBound=0)
    x_p2_w1 = LpVariable("x_p2_w1", lowBound=0)
    x_p2_w2 = LpVariable("x_p2_w2", lowBound=0)
    
    y_w1_c1 = LpVariable("y_w1_c1", lowBound=0)
    y_w1_c2 = LpVariable("y_w1_c2", lowBound=0)
    y_w1_c3 = LpVariable("y_w1_c3", lowBound=0)
    y_w1_c4 = LpVariable("y_w1_c4", lowBound=0)
    y_w2_c1 = LpVariable("y_w2_c1", lowBound=0)
    y_w2_c2 = LpVariable("y_w2_c2", lowBound=0)
    y_w2_c3 = LpVariable("y_w2_c3", lowBound=0)
    
    # 目标函数
    model += (
        0 * x_p1_w1 + 5 * x_p1_w2 + 4 * x_p2_w1 + 2 * x_p2_w2 +
        3 * y_w1_c1 + 4 * y_w1_c2 + 5 * y_w1_c3 + 4 * y_w1_c4 +
        2 * y_w2_c1 + 1 * y_w2_c2 + 2 * y_w2_c3
    )
    
    # 约束条件
    model += x_p2_w1 + x_p2_w2 <= p2_capacity  # 修改后的P2产能
    
    # 仓库流量平衡
    model += x_p1_w1 + x_p2_w1 == y_w1_c1 + y_w1_c2 + y_w1_c3 + y_w1_c4
    model += x_p1_w2 + x_p2_w2 == y_w2_c1 + y_w2_c2 + y_w2_c3
    
    # 市场需求
    model += y_w1_c1 + y_w2_c1 >= markets["c1"]["demand"]
    model += y_w1_c2 + y_w2_c2 >= markets["c2"]["demand"]
    model += y_w1_c3 + y_w2_c3 >= markets["c3"]["demand"]
    model += y_w1_c4 >= markets["c4"]["demand"]
    
    model.solve()
    
    if model.status == 1:
        return {
            "x_p1_w1": x_p1_w1.value(),
            "x_p2_w2": x_p2_w2.value(),
            "y_w1_c1": y_w1_c1.value(),
            "y_w1_c2": y_w1_c2.value(),
            "y_w1_c4": y_w1_c4.value(),
            "y_w2_c2": y_w2_c2.value(),
            "y_w2_c3": y_w2_c3.value(),
            "total_cost": model.objective.value(),
            "new_p2_capacity": p2_capacity
        }
    return None

# 求解所有场景并更新DataFrame
for scenario in scenarios:
    result = solve_scenario(scenario["new_capacity"])
    if result:
        prob_num = scenario["Problem Number"]
        
        # ChatGPT响应
        chatgpt_response = (
            f"chatgpt: The annual capacity of the Plant p2 has become {result['new_p2_capacity']:.0f}. "
            f"Therefore, the final optimal plan is as follows: "
            f"x_p1_w1: {result['x_p1_w1']:.0f}\n"
            f"x_p2_w2: {result['x_p2_w2']:.0f}\n"
            f"x_w1_c1: {result['y_w1_c1']:.0f}\n"
            f"x_w1_c2: {result['y_w1_c2']:.0f}\n"
            f"x_w1_c4: {result['y_w1_c4']:.0f}\n"
            f"x_w2_c2: {result['y_w2_c2']:.0f}\n"
            f"x_w2_c3: {result['y_w2_c3']:.0f}\n"
            f"And the total cost is {result['total_cost']:.2f}\n"
            "(请chatgpt将final optimal plan以表的形式展示，纵坐标是'w1,w2' 横坐标是'P1 P2 C1 C2 C3 C4')"
        )
        
        # DeepSeek响应
        deepseek_response = (
            f"deepseek: The annual capacity of the Plant p2 has become {result['new_p2_capacity']:.0f}. "
            f"Therefore, the final optimal plan is as follows: "
            f"x_p1_w1: {result['x_p1_w1']:.0f}\n"
            f"x_p2_w2: {result['x_p2_w2']:.0f}\n"
            f"x_w1_c1: {result['y_w1_c1']:.0f}\n"
            f"x_w1_c2: {result['y_w1_c2']:.0f}\n"
            f"x_w1_c4: {result['y_w1_c4']:.0f}\n"
            f"x_w2_c2: {result['y_w2_c2']:.0f}\n"
            f"x_w2_c3: {result['y_w2_c3']:.0f}\n"
            f"And the total cost is {result['total_cost']:.2f}\n"
            "(请deepseek将final optimal plan以表的形式展示，纵坐标是'w1,w2' 横坐标是'P1 P2 C1 C2 C3 C4')"
        )
        
        # 更新DataFrame
        df.loc[df["Problem Number"] == prob_num, "ChatGPT Response"] = chatgpt_response
        df.loc[df["Problem Number"] == prob_num, "DeepSeek Response"] = deepseek_response

# 保存更新后的Excel文件
df.to_excel(file_path, index=False)
print("结果已成功写入Excel文件")