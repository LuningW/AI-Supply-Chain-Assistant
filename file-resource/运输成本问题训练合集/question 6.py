import pandas as pd

# 30个问题列表（已替换）
questions = [
    "The per-unit shipment cost from p1 to w2 is now 3. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c3 is now 2. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w1 is now 8. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c2 is now 5. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w1 is now 7. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c4 is now 1. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w2 is now 9. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c1 is now 4. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w2 is now 1. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c2 is now 8. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w1 is now 3. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c3 is now 3. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w1 is now 4. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c1 is now 9. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w2 is now 7. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c2 is now 9. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w2 is now 6. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c3 is now 7. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w1 is now 1. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c1 is now 6. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w1 is now 2. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c4 is now 7. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w2 is now 6. How does that affect the total cost?",
    "The per-unit shipment cost from w2 to c3 is now 8. How does that affect the total cost?",
    "The per-unit shipment cost from p1 to w1 is now 9. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c1 is now 5. How does that affect the total cost?",
    "The per-unit shipment cost from p2 to w2 is now 1. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c2 is now 3. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c3 is now 9. How does that affect the total cost?",
    "The per-unit shipment cost from w1 to c4 is now 2. How does that affect the total cost?"
]

# 初始化数据列表
data = {
    "Problem Number": [],
    "Scenario Description": [],
    "ChatGPT Response": [],
    "DeepSeek Response": []
}

# 生成数据
for i, question in enumerate(questions, start=1):  # 从1到30
    for j in range(9):  # 每个问题重复9次
        data["Problem Number"].append(i)
        data["Scenario Description"].append(question if j == 0 else "")
        data["ChatGPT Response"].append("")
        data["DeepSeek Response"].append("")

# 创建DataFrame
df = pd.DataFrame(data)

# 输出到Excel
df.to_excel("output_updated.xlsx", index=False)

