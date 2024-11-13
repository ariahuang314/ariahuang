import os
import pdfplumber
from flask import current_app
import pymysql
import time
from pdf_processing.pdf_to_txt import pdf_to_clean_text # 导入 upload_pdf 函数

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'a12345678',
    'database': 'esg_database',
    'charset': 'utf8mb4'
}

def save_pdf_file(pdf_name,pdf_file):
    """将上传的 PDF 文件保存到 uploads 文件夹"""
    print("yes")
    upload_folder = 'pdf_processing/uploads'

    pdf_path = os.path.join(upload_folder, pdf_name)
    print(pdf_path)
    pdf_file.save(pdf_path)
    return pdf_path


def upload_pdf(username,industry,firm_name,country,website,year,pdf_file):
    """处理 PDF 文件的上传并返回文本内容"""
    # 保存 PDF 文件到指定目录
    pdf_name = firm_name + ' ' + year + " ESG Report " + time.strftime("%Y%m%d%H%M%S") + ".pdf"
    print(pdf_name)
    pdf_path = save_pdf_file(pdf_name,pdf_file)
    print(pdf_path)
    result =save_file_info_to_db(firm_name,username,industry,country,website,year,pdf_name,pdf_path)
    if result:
        print("Data saved successfully!")
    else:
        print("Failed to save data.")
    # 将 PDF 转换为文本
    text_content = pdf_to_clean_text(pdf_path)

    # 将文本保存到 txt_files 文件夹
    txt_folder =  'pdf_processing/txt_files'

    txt_filename = firm_name + ' ' + year + " ESG Report " + time.strftime("%Y%m%d%H%M%S") + ".txt"
    txt_path = os.path.join(txt_folder, txt_filename)
    # 确保 text_content 是字符串类型
    with open(txt_path, 'w') as txt_file:
        if isinstance(text_content, list):
            # 如果 text_content 是列表，逐行写入
            for line in text_content:
                txt_file.write(line + "\n")  # 每行后添加换行符
        else:
            # 如果 text_content 是字符串，则直接写入
            txt_file.write(text_content)

    return txt_filename,firm_name,txt_path  # 返回 txt 文件路径和文本内容

def save_file_info_to_db(firm_name,username,industry,country,website,year,pdf_name,pdf_path):
    # 将文件信息存储到数据库
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()
        query1 = "INSERT IGNORE INTO Firm (firm_name, industry,country,website) VALUES (%s, %s,%s, %s)"
        cursor.execute(query1, (firm_name, industry,country,website))
        query2 = "INSERT INTO ESG_Report (firm_name, user_name,report_name,report_year,report_path) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query2, (firm_name, username, pdf_name, year,pdf_path))
        report_id = cursor.lastrowid
        conn.commit()
        return report_id

    except Exception as e:
        print(f"Error: {e}")
        return None  # 出现异常时返回 None
    finally:
        # 关闭连接
        cursor.close()
        conn.close()