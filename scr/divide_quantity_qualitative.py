import pandas as pd
from collections import defaultdict
import json

# 读取CSV文件
csv_path = './../dictionary/dictionary_new.xlsx'
df = pd.read_excel(csv_path)

# 过滤出符合条件的定性指标
qualitative_metrics = df[df['Indicators category'] == 'Exposure']['Metric'].tolist()
# 加载字典 Excel 文件
# dictionary_df = pd.read_excel("../dictionary/dictionary_new1.xlsx")

# 初始化一个默认字典，每个指标对应多个关键词
metrics_keywords = defaultdict(list)

# 遍历每一行，将关键词加入对应的指标列表中
for _, row in df.iterrows():
    metric = row["Metric"]
    keyword = row["keyword"]
    metrics_keywords[metric].append(keyword)

# 过滤字典，仅保留 qualitative_metrics 中的指标
# filtered_metrics_keywords = {metric: keywords for metric, keywords in metrics_keywords.items() if metric in qualitative_metrics}
qualitative_metrics_keywords = {metric: metrics_keywords[metric] for metric in qualitative_metrics if metric in metrics_keywords}
quantity_metrics_keywords = {k: v for k, v in metrics_keywords.items() if k not in qualitative_metrics_keywords}


# 保存 filtered_metrics_keywords 到 JSON 文件
with open('../dictionary/qualitative_metrics_keywords.json', 'w', encoding='utf-8') as f:
    json.dump(qualitative_metrics_keywords, f, ensure_ascii=False, indent=4)

with open('../dictionary/quantity_metrics_keywords.json', 'w', encoding='utf-8') as f:
    json.dump(quantity_metrics_keywords, f, ensure_ascii=False, indent=4)

print("successful")
