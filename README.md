# groupproject
现在需要：  
大量的txt原始报告（这个容易，只需要有pdf就行）  
少量的标签报告内容（体力活）  
！！！一个会调模型的人（微笑  

###########  
目前写了pdf转换成txt, 并清洗txt  

将人工贴的标签（利用label studio）转换为标准化json  

将标准化json按照BIO标签转换为txt  

#！模型DeBERTa，基于bert的提升模型，我目前做了模型调优部分，但是不知道为什么输出是空的，我卡住了  
还需要大量的txt原始报告，和少量的标签报告内容调优  

计算指标与打分指标间的相似度 两种 这是最后模型提取结果后清洗数据的一部分，或许可信度也能用  
  基于TF-IDF向量化  
  基于bert词嵌入  
