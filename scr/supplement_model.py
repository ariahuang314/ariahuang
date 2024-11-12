import re
from transformers import pipeline
from collections import defaultdict
import pandas as pd
import json

outputfile = '../output_metric/Qualitative_metrics.csv'

def load_supplement_model(file):
    with open('../dictionary/qualitative_metrics_keywords.json', 'r', encoding='utf-8') as f:
        qualitative_metrics_keywords = json.load(f)
    # 情感分析模型
    sentiment_analyzer = pipeline('sentiment-analysis', model="distilbert-base-uncased-finetuned-sst-2-english")

    # metrics_keywords变量示例
    qualitative_metrics_keywords = defaultdict(list, qualitative_metrics_keywords)


    with open(file, 'r') as file:
        raw_text = file.read()

    # 存储匹配结果
    results = []

    # 遍历metrics_keywords中的每个指标及其关键词
    for metric, keywords in qualitative_metrics_keywords.items():
        found = False  # 标记是否找到匹配的关键词
        for keyword in keywords:
            if found:
                break  # 如果已经找到匹配项，则跳出循环
            keyword_pattern = re.escape(str(keyword))
            # match = re.search(rf"([^.]*?\b({keyword_pattern})\b[^.]*\.)", raw_text)
            match = re.search(rf"([^.]*?({keyword_pattern})[^.]*\.)", raw_text)

            if match:
                sentence = match.group(0)
                matched_keyword = match.group(2)  # 提取匹配的具体关键字
                
                # 将句子按句号分割，逐段分析
                sub_sentences = re.split(r'(?<=\.) ', sentence)
                for sub_sentence in sub_sentences:
                    if len(sub_sentence) > 512:  # 如果子句仍然过长则截断
                        sub_sentence = sub_sentence[:512]

                    # 进行情感分析
                    sentiment = sentiment_analyzer(sub_sentence)
                    confidence = sentiment[0]['score']
                    sentiment_label = sentiment[0]['label']
                    
                    # 记录结果
                    results.append({
                        'metric': metric,
                        'keyword': matched_keyword,
                        # 'sentence': sub_sentence,
                        'sentiment': sentiment_label,
                        'confidence': confidence
                    })
                    
                found = True  # 标记找到匹配项，退出关键词循环

    # 从results中提取Metric列，并将Value列设为1
    metrics_data = [{'metric': result['metric'], 'value': 1, 'confidence':result['confidence']} for result in results]

    # 创建新的DataFrame
    metrics_df = pd.DataFrame(metrics_data).drop_duplicates()  # 去重，避免重复的Metric
    outputfile = '../output_metric/Qualitative_metrics.csv'
    metrics_df.to_csv(outputfile, index=False)
    print('qualitative metric successful')



