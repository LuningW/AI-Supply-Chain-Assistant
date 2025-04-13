import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import openai  # 你已有的 openai 导入方式
from tqdm import tqdm

# ✅ 如果你原本用环境变量读取 key，那这一行不变
openai.api_key = ""  # 请替换为你的 key

# 设置文件路径-可换
# QR问题合集/qr_policy_prompt_card.xlsx
# 生产计划问题合集/production_plan_prompt_cards.xlsx
# 运输成本问题训练合集/transport_prompt_cards.xlsx
INPUT_PATH = "file-resource/运输成本问题训练合集/transport_prompt_cards.xlsx"
OUTPUT_PATH = "file-resource/运输成本问题训练合集/transport_similarity_result.xlsx"


## 读取数据
df = pd.read_excel(INPUT_PATH)

# ✅ 正确的分组逻辑：每10行为一组
df["Group Index"] = df.index // 10

# 获取前5组（你可以改成全部 group_ids = list(df["Group Index"].unique())）
group_ids = sorted(df["Group Index"].unique())
grouped = df.groupby("Group Index")

# 新版 OpenAI Embedding 接口（>=1.0.0）
def get_embeddings(sentences, model="text-embedding-ada-002"):
    response = openai.embeddings.create(input=sentences, model=model)
    return [item.embedding for item in response.data]

# 结果存储
results = []

for gid in tqdm(group_ids, desc="Checking all groups..."):
    group = grouped.get_group(gid)
    sentences = group["User Question"].tolist()
    problem_numbers = group["Problem Number"].tolist()

    try:
        embeddings = get_embeddings(sentences)
        sim_matrix = cosine_similarity(embeddings)
        avg_sim = (sim_matrix.sum() - len(sentences)) / (len(sentences) * (len(sentences) - 1))

        if avg_sim > 0.95:
            label = "Severe Redundancy"
        elif avg_sim > 0.85:
            label = "Mild Redundancy"
        else:
            label = "Good"

        results.append({
            "Group Index": gid,
            "Problem Number Range": f"{min(problem_numbers)}–{max(problem_numbers)}",
            "Avg Similarity": round(avg_sim, 4),
            "Rewrite Status": label
        })

    except Exception as e:
        print(f"⚠️ Embedding failed for Group {gid}: {e}")
        results.append({
            "Group Index": gid,
            "Problem Number Range": f"{min(problem_numbers)}–{max(problem_numbers)}",
            "Avg Similarity": None,
            "Rewrite Status": "Failed"
        })

# 保存结果
pd.DataFrame(results).to_excel(OUTPUT_PATH, index=False)
print(f"\n✅ 检查完成，结果已保存到: {OUTPUT_PATH}")