
import pandas as pd
from sqlalchemy import create_engine

def save_db():
    # 读取本地 CSV 文件
    csv_file_path = '../output_metric/metrics_filter.csv' # 替换为您的 CSV 文件路径
    df_unique = pd.read_csv(csv_file_path)

    # 修改列名，使其与数据库表的列名一致
    df_unique = df_unique.rename(columns={
        'company_name': 'company_name',
        'standard_metric': 'metric',
        'value': 'value',
        'unit': 'unit',
        'similarity': 'similiarity',
        'confidence': 'confidence'
    })

    # 数据库配置信息
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'database5105',
        'charset': 'utf8mb4'
    }

    # 创建数据库连接字符串
    connection_str = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}?charset={db_config['charset']}"

    # 创建 SQLAlchemy 引擎
    engine = create_engine(connection_str)

    # 将修改后的数据存入 MySQL 数据库表中
    df_unique.to_sql(
        name='structured_data',      # 替换为您的表名
        con=engine,
        if_exists='append',          # 'append' 将数据追加到已有表
        index=False                  # 不将 DataFrame 的索引存入数据库
    )

    print("df upload to database sucessfully")

