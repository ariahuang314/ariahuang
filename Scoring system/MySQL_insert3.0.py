import pandas as pd
import pymysql
import os

# 数据库配置
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '259381xX/',
    'database': 'database5105',
    'charset': 'utf8mb4'
}

# CSV 文件夹路径
csv_folder_path = '../database3.0/insert/'

# 获取文件夹中的 CSV 文件
csv_files = sorted([f for f in os.listdir(csv_folder_path) if f.endswith('.csv')])

# 插入数据的 SQL 语句

insert_structured_data = """
INSERT INTO structured_data (company_name, metric, value, unit)
VALUES (%s, %s, %s, %s)
"""


try:
    # 连接到 MySQL 数据库
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor()

    # 循环遍历文件并插入到structured_data表
    for file in csv_files[3:4]:
        df = pd.read_csv(os.path.join(csv_folder_path, file), encoding='ISO-8859-1')
        df.columns = df.columns.str.strip()
        df = df.where(pd.notnull(df), None)

        values_scores = [
            (row['company_name'], row['metric'], row['value'], row['unit'])
            for _, row in df.iterrows()
        ]

        cursor.executemany(insert_structured_data, values_scores)

    # 提交更改
    conn.commit()
    print("Records inserted successfully into ESG_Report and ESG_Scores tables.")

except pymysql.MySQLError as e:
    print(f"Error: {e}")
    conn.rollback()  # 回滚未提交的更改

finally:
    # 关闭连接
    cursor.close()
    conn.close()
    print("MySQL connection is closed.")



