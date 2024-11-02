# groupproject  
目前剩下的任务：  
1. 利用模型将txt文件转换为grouped_data.json格式的内容，可以在我的基础上调，换模型也行  
直接尝试表格提取工具（pdfplumber，tabula）或者正则化也可以
(可以有缺失值unit)   
2. 行业迁移  
最后整个项目跑遍，把环境下载下来  
**有代码更新记得传github,单独开branch,项目快截止了，还要前后端连接，创建docker, wiki,ppt**  
**你们三个人分一下上面的任务吧，我去算可信度**  

我觉得模型可能需要：  
少量的标签报告内容（体力活）    

#### 代码内容
写在前面，所有的input output文件名有些只包含了前半部分  
eg: grouped_data.json 代表目前所有以grouped_data开头和.json结尾的文件 如: grouped_data_full.json  
后半部分不同有时只是数据量不同  

之前的output/1030.txt删除了，内容和AML一样，txt/AML.txt为清洗完全版本  

- scr/pdf_to_txt.ipynb  
将pdf转换成txt, 并清洗txt  
可以处理单个pdf文件或者整个文件夹以下的所有pdf  
  - input: data/file.pdf  
  - output: txt/file.pdf  

- scr/transform_json.ipynb  
将从人工贴的标签（利用label studio）转换为标准化json格式  
  - format:{ "metric":  "value":  "unit": }  
  - input: json/project-full.json  
  - output: json/grouped_data.json  

- scr/ESG_metric_LLM2.ipynb   
第一个部分：将标准化json按照BIO标签转换为txt  
BIO标签是bert学习的格式
  - format:Net B-INDICATOR profit I-INDICATOR 1.9 B-VALUE S$ B-UNIT million I-UNIT
  - input: json/grouped_data.json  
  - output: output/bio_data.json  

之后部分：调用模型DeBERTa（基于bert的提升模型）  
目前包含模型调优，模型训练，保存模型，调用调优模型  
**但是不知道为什么输出是空的,你们可以在此基础上调优或者替换模型，我确实调不出来了**  
  - input:  
    json_filepath = '../json/grouped_data_full1.json'  
    bio_filepath = '../output/bio_data.txt'  
    raw_text_filepath = '../txt/AML.txt'   
  - output: output_metric/esg_data.csv  最好还是json,便于后续代码，当时写的时候没注意，输出格式要和grouped_data.json一致,最好加个来源  
  - output: model/fine_tuned_deberta  调优模型，因为太大了我没上传  

- scr/simiarlity.ipynb  
用于清洗LLM输出的json,只留下B组需要的指标  
计算报告中指标与B组打分指标间的相似度，**（并计算指标可信度，我正在写）**  
包含两种 高精度 和 高速度 模式的相似度  
  - input: json/grouped_data.json   **之后替换为LLM输出**   
  - output: json/filtered_data_bert.json  基于bert词嵌入  
  - output: json/filtered_data.json  基于TF-IDF向量化   

#### 关于csv和xlsx
- dictionary.xlsx 是之前提供的字典，列分别为：一级二级三级标题，关键词（可能是三级标题近义词），GRI  
- output/unique_metric.csv  根据dictionary.xlsx提出的唯一三级标题  
