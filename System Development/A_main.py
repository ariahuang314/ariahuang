import importlib


from .pdf_processing.upload_pdf import upload_pdf
from .supplement_model import load_supplement_model
from .llm_model import load_llm_model
from .merge_similarity import merge_metric
from .merge_similarity import calculate_simliarity
from .save_to_db import save_db
from .scoring_code import scoring_metric
import os
def main(username,selected_industry,firm_name,country,website,year,file):
    username=username
    selected_industry=selected_industry
    firm_name=firm_name
    country=country
    website=website
    print("Starting main function...")
    print(
        f"Parameters received: username={username}, industry={selected_industry}, firm_name={firm_name}, country={country}, website={website}, year={year}")
    print(f"File: {file.filename if file else 'No file provided'}")

    # 确保当前目录正确
    current_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(current_path)
    print("Current path set to:", current_path)


    # 定义文件夹名称列表
    folders = ['output_metric']
    for folder in folders:
        folder_path = os.path.join("../", folder)  # 指定上级目录的路径
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)  # 使用完整的路径创建文件夹

    # 调用函数并传递参数
    filename, companyname, filepath = upload_pdf(username,selected_industry,firm_name,country,website,year,file)
    print(filename, companyname, filepath)
    filepath='./'+ filepath
    load_llm_model(filepath)
    load_supplement_model(filepath)
    merge_metric(companyname)
    calculate_simliarity()
    save_db()
    scoring_metric()
    print("Running main.py")




