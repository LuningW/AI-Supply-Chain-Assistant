import pandas as pd

# 修正后的列顺序配置
COLUMN_ORDER = [
    "Problem Number",
    "Scenario Description",
    "ChatGPT Response",  # 第三列
    "DeepSeek Response"   # 第四列
]

# 原始问题数据集（保持不变）
question_data = [
    (30, 90, 27), (31, 95, 36), (32, 99, 52), (33, 91, 31), (34, 96, 42),
    (35, 92, 35), (36, 97, 48), (37, 93, 39), (38, 98, 55), (39, 94, 42),
    (40, 90, 36), (41, 95, 47), (42, 91, 40), (43, 96, 53), (44, 99, 71),
    (45, 92, 45), (46, 97, 61), (47, 93, 49), (48, 98, 69), (49, 94, 53),
    (50, 90, 45), (30, 96, 37), (31, 99, 51), (32, 91, 30), (33, 97, 44),
    (34, 95, 40), (35, 98, 51), (36, 94, 39), (37, 92, 37), (38, 93, 40)
]

def generate_corrected_data():
    """生成修正列顺序后的数据"""
    formatted_data = []
    
    for idx, (sigma, sl, ans) in enumerate(question_data, 1):
        scenario = f"When the standard deviation is {sigma} tables, what is the safety stock with a service level of {sl}%?"
        
        # 每个问题生成9行，交换响应列位置
        for _ in range(9):
            row = {
                "Problem Number": idx,
                "Scenario Description": scenario,
                "ChatGPT Response": f"chatgpt: When σ = {sigma} and service level is {sl}%, safety stock is {ans} tables.",  # 第三列
                "DeepSeek Response": f"deepseek: When σ = {sigma} and service level is {sl}%, safety stock is {ans} tables."   # 第四列
            }
            formatted_data.append(row)
    
    return pd.DataFrame(formatted_data)[COLUMN_ORDER]  # 确保列顺序

# 生成并保存文件
df_corrected = generate_corrected_data()
df_corrected.to_excel(
    "plan-questions-set1-corrected.xlsx",
    index=False,
    engine="openpyxl"
)

print("修正版文件已生成，列顺序验证：")
print(df_corrected.iloc[0][COLUMN_ORDER])  # 打印首行验证列顺序
