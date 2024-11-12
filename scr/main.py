import importlib
import llm_model
importlib.reload(llm_model)

from pdf_to_txt import load_file
from supplement_model import load_supplement_model
from llm_model import load_llm_model
from merge_similarity import merge_metric
from merge_similarity import calculate_simliarity
from save_to_db import save_db
from scoring_code import scoring_metric
import os

current_path = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_path)

# 定义文件夹名称列表
folders = ['upload','output_metric', 'txt']
for folder in folders:
    folder_path = os.path.join("../", folder)  # 指定上级目录的路径
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)  # 使用完整的路径创建文件夹

# 调用函数并传递参数
filename, companyname, filepath = load_file()
load_llm_model(filepath)
load_supplement_model(filepath)
merge_metric(companyname)
calculate_simliarity()
save_db()
scoring_metric()


