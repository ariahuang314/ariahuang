import pandas as pd
import json
from transformers import BertTokenizer, BertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

quan = '../output_metric/Quantity_metrics.csv'
quan_filter = '../output_metric/Quantity_metrics_filter.csv'

qual = '../output_metric/Qualitative_metrics.csv'
qual_filter = '../output_metric/Qualitative_metrics_filter.csv'

merge = '../output_metric/metrics.csv'
merge_filter = '../output_metric/metrics_filter.csv'

def merge_metric(companyname='default'):
    
    df_quan = pd.read_csv(quan)
    df_qual = pd.read_csv(qual)

    df_quan.columns = df_quan.columns.str.lower()
    df_qual.columns = df_qual.columns.str.lower()

    # 按行合并，自动处理列名不一致的情况
    merged_df = pd.concat([df_quan, df_qual], axis=0, ignore_index=True)
    merged_df['company_name'] = companyname

    # 保存合并后的文件
    merged_df.to_csv(merge, index=False, encoding='utf-8-sig')


def calculate_simliarity():
    # 加载BERT模型和分词器
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', cache_dir='./cache')
    model = BertModel.from_pretrained('bert-base-uncased', cache_dir='./cache')

    # 定义函数获取BERT嵌入并显示进度条
    def get_bert_embeddings_with_progress(text_list, description="Calculating embeddings"):
        embeddings = []
        for text in tqdm(text_list, desc=description):
            inputs = tokenizer(text, return_tensors='pt', truncation=True, max_length=128, padding='max_length')
            with torch.no_grad():
                outputs = model(**inputs)
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
            embeddings.append(embedding)
        return embeddings

    # 加载CSV文件
    data_source = merge  # 数据源路径
    data = pd.read_csv(data_source)

    # 从CSV提取 `metric`、`value` 和 `unit`
    company_name = data['company_name'].tolist()
    raw_metrics = data['metric'].tolist()
    json_values = data['value'].tolist()
    json_units = data['unit'].tolist()
    json_confident = data['confidence'].tolist()

    # 加载目标标签的CSV文件
    csv_data = pd.read_excel('../dictionary/dictionary_new.xlsx')
    target_labels = csv_data['keyword'].dropna().unique().tolist()

    # 获取BERT嵌入
    json_embeddings = get_bert_embeddings_with_progress(raw_metrics, "Calculating metrics embeddings")
    target_embeddings = get_bert_embeddings_with_progress(target_labels, "Calculating target label embeddings")

    # 设置相似度阈值
    similarity_threshold = 0.7
    filtered_data = []

    # 比较每个 metric 和目标标签的相似度，并筛选数据
    for i, raw_metric in tqdm(enumerate(raw_metrics), desc="Calculating similarities", total=len(raw_metrics)):
        similarities = cosine_similarity([json_embeddings[i]], target_embeddings).flatten()
        max_similarity_index = similarities.argmax()
        max_similarity = similarities[max_similarity_index]
        
        if max_similarity >= similarity_threshold:
            matched_label = target_labels[max_similarity_index]
            standard_metric = csv_data.loc[csv_data['keyword'] == matched_label, 'Metric'].iloc[0]
            
            # 将 metric, value, unit, key_word, standard_metric 和 similarity 添加到筛选后的数据
            filtered_entry = {
                'company_name': company_name[i],
                # 'raw_metric': raw_metric,
                'standard_metric': standard_metric,
                'value': json_values[i],
                'unit': json_units[i],
                # 'key_word': matched_label,
                'similarity': float(max_similarity),
                'confidence': json_confident[i]
            }
            filtered_data.append(filtered_entry)

    filtered_data = pd.DataFrame(filtered_data)

    df_unique = (
        filtered_data.sort_values(by=['standard_metric', 'similarity', 'confidence'], ascending=[True, False, False])
        .drop_duplicates(subset='standard_metric', keep='first')
    )

    with open('../dictionary/qualitative_metrics_keywords.json', 'r', encoding='utf-8') as f:
        qualitative_metrics_keywords = json.load(f)

    # 假设 qualitative_metrics_keywords 是包含要匹配的 metric 的集合或列表
    qualitative_metrics_keywords = set(qualitative_metrics_keywords)  # 确保是集合类型，提高查找效率

    # 使用 loc 来修改 df_unique 中符合条件的行
    df_unique.loc[df_unique['standard_metric'].isin(qualitative_metrics_keywords), 'value'] = 1

    # 清洗数据，删除 'value' 列中非数字的行
    df_unique['value'] = pd.to_numeric(df_unique['value'], errors='coerce')  # 将非数字转换为 NaN
    df_unique = df_unique.dropna(subset=['value'])  # 删除 'value' 列中为 NaN 的行

    # （可选）将 'value' 列转换回整数或浮点数类型，取决于您的需求
    df_unique['value'] = df_unique['value'].astype(float)  # 或者 int 类型

    # 查看结果
    # print(df_unique)

    # 保存结果为CSV文件
    df_unique = pd.DataFrame(df_unique)
    df_unique.to_csv(merge_filter, index=False, encoding='utf-8-sig')
    print("Filtering is complete.csv")
