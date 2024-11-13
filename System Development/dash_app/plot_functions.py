import plotly.express as px
import pandas as pd
import pymysql
import yfinance as yf
from flask import session, request
import numpy as np
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
from plotnine import *
import geopandas as gpd

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'a12345678',
    'database': 'esg_database',
    'charset': 'utf8mb4'
}

conn = pymysql.connect(**db_config)
cursor = conn.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM ESG_Scores ORDER BY score_id DESC LIMIT 1"
cursor.execute(sql)

# 获取结果并转换为 DataFrame
result = cursor.fetchone()
conn.close()

df = pd.DataFrame([result])





def get_score():
    # 假设从数据源加载数据
     # 例如，获取数据的自定义函数

    # 检查和转换每个评分列。如果缺少某列，则为其添加默认值
    for column in ['Total_Score', 'E_Score', 'S_Score', 'G_Score']:
        if column not in df.columns:
            print(f"Warning: '{column}' column is missing. Setting default value to 0.")
            df[column] = 0  # 设置默认值
        else:
            # 转换为数值类型
            df[column] = pd.to_numeric(df[column], errors='coerce')

    # 提取每个分数列
    total_score = df['Total_Score']
    e_score = df['E_Score']
    s_score = df['S_Score']
    g_score = df['G_Score']

    return total_score, e_score, s_score, g_score
# ESG 等级判定函数
def determine_esg_level():
    total_score, _, _, _ = get_score()
    # 如果 total_score 是一个 Series，确保只提取单一值
    if isinstance(total_score, pd.Series):
        total_score = total_score.iloc[0]  # 提取第一个数值
    elif isinstance(total_score, (list, np.ndarray)):
        total_score = total_score[0]  # 如果是列表或数组，也提取第一个数值

    if total_score >= 85.72:
        return "AAA"
    elif total_score >= 71.44:
        return "AA"
    elif total_score >= 57.15:
        return "A"
    elif total_score >= 42.87:
        return "BBB"
    elif total_score >= 28.68:
        return "BB"
    elif total_score >= 14.30:
        return "B"
    else:
        return "CCC"


# 仪表盘
def create_gauge():
    total_score, _, _, _ = get_score()
    # 如果 total_score 是一个 Series，确保只提取单一值
    if isinstance(total_score, pd.Series):
        total_score = total_score.iloc[0]  # 提取第一个数值
    elif isinstance(total_score, (list, np.ndarray)):
        total_score = total_score[0]  # 如果是列表或数组，也提取第一个数值

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_score,
        title={'text': "ESG Score", 'font': {'size': 20}},  # 调整标题字体大小
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "darkgreen", 'thickness': 0.2},  # 调整指针的粗细
            'bgcolor': "white",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': "white"},
                {'range': [40, 60], 'color': "lightgreen"},
                {'range': [60, 80], 'color': "limegreen"},
                {'range': [80, 100], 'color': "green"},
            ],
        },
        domain={'x': [0.1, 0.9], 'y': [0, 0.75]}  # 缩小仪表的显示范围
    ))

    fig_gauge.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),dragmode=False,hovermode=False  # 去除外边距
    )

    return fig_gauge

# 获取股票数据

# 创建e_score环状图
def create_doughnut_chart():
    _, e_score, _, _ = get_score()
    e_score = float(e_score.iloc[0].round(2))  # Convert to float with two decimal places
    remain_e_score = round(33.53 - e_score, 2)

    fig_doughnut_chart_e = go.Figure()

    # Create the doughnut chart
    fig_doughnut_chart_e.add_trace(go.Pie(
        labels=["E Score", ""],  # Labels
        values=[e_score, remain_e_score],  # Score and remaining score
        hole=0.5,  # Adjusted hole size for a fuller chart
        marker=dict(colors=["#228B22", "#DCDCDC"]),  # Set color for score part
        showlegend=False,  # Disable legend
        textinfo="none",  # Hide default text, use custom text instead
        hoverinfo="label+value",  # Display label and score on hover
        rotation=210
    ))

    # Add "E Score" label at the center
    fig_doughnut_chart_e.update_layout(
        annotations=[
            dict(
                text="E Score",
                x=0.5, y=0.5,
                font=dict(size=30, color="black"),
                showarrow=False
            ),
            # Place the score at the bottom center of the chart
            dict(
                text=str(e_score),  # Display the score value
                x=0.5, y=0.25,  # Adjust y to control vertical position
                font=dict(size=28, color="black"),
                showarrow=False
            )
        ],
        margin=dict(t=5, b=5, l=5, r=5)  # Reduce margins
    )

    return fig_doughnut_chart_e


def create_doughnut_chart_s():
    # 从数据库中获取数据
    _, _, s_score, _ = get_score()  # 假设 get_score() 是一个数据库查询函数

    # 调试输出，确保查询结果有效
    print(f"Retrieved S score: {s_score}")

    # 如果 s_score 是空的，或者包含无效值，则返回一个空的图表
    if s_score is None or s_score.empty or s_score.iloc[0] is None:
        return go.Figure()  # 返回一个空的图表，避免显示空白

    # 将 s_score 转换为浮动类型，并保留两位小数
    s_score = float(s_score.iloc[0].round(2))  # Convert to float with two decimal places
    remain_s_score = round(45.90 - s_score, 2)

    # 创建圆环图
    fig_doughnut_chart_s = go.Figure()

    fig_doughnut_chart_s.add_trace(go.Pie(
        labels=["S Score", ""],  # Labels
        values=[s_score, remain_s_score],  # Score and remaining score
        hole=0.5,  # Adjusted hole size for a fuller chart
        marker=dict(colors=["#228B22", "#DCDCDC"]),  # Set color for score part
        showlegend=False,  # Disable legend
        textinfo="none",  # Hide default text, use custom text instead
        hoverinfo="label+value",  # Display label and score on hover
        rotation=210
    ))

    # Add "S Score" label at the center
    fig_doughnut_chart_s.update_layout(
        annotations=[
            dict(
                text="S Score",
                x=0.5, y=0.5,
                font=dict(size=30, color="black"),
                showarrow=False
            ),
            # Place the score at the bottom center of the chart
            dict(
                text=str(s_score),  # Display the score value
                x=0.5, y=0.25,  # Adjust y to control vertical position
                font=dict(size=28, color="black"),
                showarrow=False
            )
        ],
        margin=dict(t=5, b=5, l=5, r=5),
        height=350 # Reduce margins
    )

    return fig_doughnut_chart_s

def create_doughnut_chart_g():
    _, _, _, g_score = get_score()
    g_score = float(g_score.iloc[0].round(2))  # Convert to float with two decimal places
    remain_g_score = round(20.57 - g_score, 2)

    fig_doughnut_chart_g = go.Figure()

    # Create the doughnut chart
    fig_doughnut_chart_g.add_trace(go.Pie(
        labels=["G Score", ""],  # Labels
        values=[g_score, remain_g_score],  # Score and remaining score
        hole=0.5,  # Adjusted hole size for a fuller chart
        marker=dict(colors=["#228B22", "#DCDCDC"]),  # Set color for score part
        showlegend=False,  # Disable legend
        textinfo="none",  # Hide default text, use custom text instead
        hoverinfo="label+value",  # Display label and score on hover
        rotation=350
    ))

    # Add "E Score" label at the center
    fig_doughnut_chart_g.update_layout(
        annotations=[
            dict(
                text="G Score",
                x=0.5, y=0.5,
                font=dict(size=30, color="black"),
                showarrow=False
            ),
            # Place the score at the bottom center of the chart
            dict(
                text=str(g_score),  # Display the score value
                x=0.5, y=0.25,  # Adjust y to control vertical position
                font=dict(size=28, color="black"),
                showarrow=False
            )
        ],
        margin=dict(t=5, b=5, l=5, r=5)  # Reduce margins
    )

    return fig_doughnut_chart_g


def create_bar_chart():

    values=df.iloc[-1].to_dict()
    e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
    s_metrics = ['Employees_covered_by_health_insurance',
        'Company_donated', 'Avg_training_hours_per_employee', 'Employees_above_50', 'Female_employees',
        'Employee_satisfaction_rate', 'New_hires_female', 'New_hires_above_50', 'Total_turnover','Turnover_female',
        'Turnover_above_50','Fatalities', 'High_consequence_injuries',
        'Work_related_injuries']
    g_metrics = ['Board_independence', 'Women_in_management_team', 'Women_on_board']
    metrics = e_metrics + s_metrics + g_metrics, e_metrics
    # 分别计算E、S、G的值和颜色
    e_values = [values[metric] for metric in e_metrics]
    s_values = [values[metric] for metric in s_metrics]
    g_values = [values[metric] for metric in g_metrics]

    # 创建柱状图
    fig_bar_chart = go.Figure()

    # E的柱状图 (浅绿色)
    fig_bar_chart.add_trace(go.Bar(
        x=e_metrics,
        y=e_values,
        name='E (Environment)',
        marker=dict(color='lightgreen'),
        text=e_values,  # 在柱子上显示数值
        textposition='auto',  # 自动显示在柱子上
    ))

    # S的柱状图 (绿色)
    fig_bar_chart.add_trace(go.Bar(
        x=s_metrics,
        y=s_values,
        name='S (Social)',
        marker=dict(color='lightblue'),
        text=s_values,  # 在柱子上显示数值
        textposition='auto',  # 自动显示在柱子上
    ))

    # G的柱状图 (深绿色)
    fig_bar_chart.add_trace(go.Bar(
        x=g_metrics,
        y=g_values,
        name='G (Governance)',
        marker=dict(color='darkgreen'),
        text=g_values,  # 在柱子上显示数值
        textposition='auto',  # 自动显示在柱子上
    ))

    # 更新布局
    fig_bar_chart.update_layout(
        title='E, S, G Indicators Bar Chart',
        barmode='group',  # 分组柱状图
        xaxis=dict(title='Metrics', tickangle=45),  # X轴设置
        showlegend=True,  # 显示图例
        margin=dict(t=40, b=100, l=40, r=40),  # 设置边距
        font = dict(size = 14),
        plot_bgcolor='white',  # 绘图区背景颜色
        paper_bgcolor='white'  # 整个图表背景颜色
    )

    return fig_bar_chart

def map():
    world = gpd.read_file("../config/wk11_worldmap.geojson")
    cities = gpd.read_file("../config/wk11_cities.geojson")
    singapore = cities[cities["Country"] == "Singapore"]
    us = world[world["SOV_A3"] == "US1"]
    china = world[world["SOV_A3"] == "CH1"]
    fig, ax = plt.subplots(frameon=False)
    world.plot(color="white", edgecolor="lightgray", ax=ax, legend=False)
    singapore.plot(color="limegreen", marker="o", markersize=30, ax=ax)
    us.plot(color="limegreen", ax=ax)
    china.plot(color="limegreen", ax=ax)
    ax.set_axis_off()

    # 将图像保存到缓冲区并转换为 base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    return image_base64


def generate_summary_investors():
    # Calculate esg_level
    total_score, e_score, s_score, g_score = get_score()
    total_score = total_score.iloc[0]
    e_score = e_score.iloc[0]
    s_score = s_score.iloc[0]
    g_score = g_score.iloc[0]
    esg_level = determine_esg_level()
    e_avg = 20.81
    s_avg = 18.89
    g_avg = 12.47
    # indicators
    e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
    s_metrics = ['Employee_satisfaction_rate', 'Turnover_by_gender', 'Turnover_by_age']
    g_metrics = ['Board_independence', 'Women_in_the management_team', 'Women_on_the_board']
    # average of indicators
    e_avg_metrics = {'Emission_intensities': 0.12, 'Energy_consumption_intensity': 1.96, 'Waste_generated': 339.90,
                     'Water_intensity': 1.84}
    s_avg_metrics = {'Employee_satisfaction_rate': 80, 'Turnover_by_gender': 65.42, 'Turnover_by_age': 16.28}
    g_avg_metrics = {'Board_independence': 60, 'Women_in_the management_team': 42.34, 'Women_on_the_board': 29.68}
    # Default recommendation: for companies with scores above the industry average.
    e_text = f"The score of environmental performance is {e_score.round(2)}."
    e_advice = (
        "The company's environmental performance exceeds the industry average, indicating strong sustainability practices. \n"
        "However, investors should stay attentive to changes in industry regulations and policies. \n"
        "As evolving standards may impact the company's environmental strategies and compliance requirements over time."
    )

    s_text = f"The score of social performance is {s_score.round(2)}."
    s_advice = (
        "The company's social performance surpasses the industry average, reflecting strong relationships with employees, customers, and communities.\n"
        "Investors are encouraged to consider this as a positive factor, \n"
        "but should continue monitoring social metrics to ensure the company maintains high standards in workforce satisfaction and other metrcis."
    )

    g_text = f"The score of governance performance is {g_score.round(2)}."
    g_advice = (
        "The company's governance performance is above industry average, reflecting strong management and accountability. "
        "Investors should monitor governance practices regularly to ensure they continue to align with best practices and protect shareholder interests."
    )

    # Different scenarios
    # Scenario1: e_score > e_avg and s_score > s_avg and g_score > g_avg
    if e_score > e_avg and s_score > s_avg and g_score > g_avg:
        e_text = f"The score of environmental performance is {e_score.round(2)}, which is higher than the average level of the healthcare industry."
        s_text = f"The score of social performance is {s_score.round(2)}, which is higher than the average level of the healthcare industry."
        g_text = f"The score of governance performance is {g_score.round(2)}, which is higher than the average level of the healthcare industry."

        # Step1: Identify the relatively lowest score among three scores
        lowest_score = min(e_score / 33.53, s_score / 45.90, g_score / 20.57)
        # Situation1
        if lowest_score == e_score / 33.53:
            # find the e_metrcis that are lower than industy average
            low_e_metrics = [metric for metric in e_metrics if df[metric].iloc[-1] < e_avg_metrics[metric]]
            if low_e_metrics:
                e_advice = (
                        "Although the overall environmental score is satisfactory, the following environmental indicators are below industry average: "
                        + ", ".join(low_e_metrics) + ". "
                                                     "It is advisable for investors to pay attention to these areas in order to mitigate potential risks."
                )
            else:
                e_advice = (
                    "The company's environmental performance exceeds the industry average, indicating strong sustainability practices. \n"
                    "However, investors should stay attentive to changes in industry regulations and policies. \n"
                    "As evolving standards may impact the company's environmental strategies and compliance requirements over time."
                )

        # Situation2
        if lowest_score == s_score:
            # Identify social indicators of interest to investors that are below industry averages
            low_s_metrics = [metric for metric in s_metrics if df[metric].iloc[-1] < s_avg_metrics[metric]]
            low_s_metrics = []

            # Employee satisfaction rate
            if df['Employee_satisfaction_rate'].iloc[-1] < s_avg_metrics['Employee_satisfaction_rate']:
                low_s_metrics.append('Employee_satisfaction_rate')

            # Turnover by gender (female) and Turnover by age (aged above 50 years old)
            if df['Turnover_by_gender'].iloc[-1] > s_avg_metrics['Turnover_by_gender']:
                low_s_metrics.append('Turnover_by_gender')

            if df['Turnover_by_age'].iloc[-1] > s_avg_metrics['Turnover_by_age']:
                low_s_metrics.append('Turnover_by_age')

            if low_s_metrics:
                s_advice = (
                        "Although the overall social score is satisfactory, the following social indicators are below industry average: "
                        + ", ".join(low_s_metrics) + ". "
                                                     "Investors should monitor these areas for potential social impact risks."
                )
            else:
                s_advice = (
                    "The company's social performance surpasses the industry average, reflecting strong relationships with employees, customers, and communities.\n"
                    "Investors are encouraged to consider this as a positive factor, \n"
                    "but should continue monitoring social metrics to ensure that the company maintains high standards in workforce satisfaction and community engagement over time."
                )

        # Situation3
        if lowest_score == g_score:
            low_g_metrics = [metric for metric in g_metrics if df[metric].iloc[-1] < g_avg_metrics[metric]]

            if low_g_metrics:
                g_advice = (
                        "Although the overall governance score is satisfactory, the following governance indicators are below industry average: "
                        + ", ".join(low_g_metrics) + ". "
                                                     "It is advisable for investors to focus on these specific governance areas to mitigate potential risks."
                )
            else:
                g_advice = (
                    "The company's governance performance is above industry average, reflecting strong management and accountability. \n"
                    "Investors should monitor governance practices regularly to ensure they continue to align with best practices and protect shareholder interests."
                )

    # Scenario2
    elif e_score > e_avg and s_score > s_avg and g_score <= g_avg:
        g_advice = (
            "The company demonstrates strong performance in environmental and social aspects, suggesting good sustainability practices and a positive impact on society.\n "
            "However, governance performance is below the industry average, which may pose potential risks in areas such as transparency, accountability, and decision-making.\n "
            "Investors are advised to carefully assess the company's governance structures, board diversity, and executive accountability measures to mitigate possible risks. \n"
            "Monitoring compliance with ethical standards and industry regulations is also recommended to ensure long-term stability and shareholder value."
        )

    elif e_score > e_avg and s_score <= s_avg and g_score > g_avg:
        s_advice = (
            "The company shows strong performance in environmental and governance aspects, indicating sound sustainability practices and effective management structures.\n"
            "However, social performance is below the industry average, which may point to challenges in areas such as employee satisfaction, workplace safety, and community relations.\n"
            "Investors are advised to assess the company's approach to social responsibility, including employee well-being, diversity, and community relations.\n"
        )

    elif e_score <= e_avg and s_score > s_avg and g_score > g_avg:
        e_advice = (
            "The company exhibits strong performance in social and governance aspects, suggesting effective management structures and a commitment to employee and community well-being.\n"
            "However, environmental performance is below the industry average, which may indicate potential risks related to resource management, carbon emissions, or waste management practices.\n"
            "Investors should evaluate the company's environmental policies and performance, including emissions reduction, energy efficiency, and waste management.\n"
        )

    # Scenario3
    elif e_score > e_avg and s_score <= s_avg and g_score <= g_avg:
        s_advice = (
            "The company shows strong performance in environmental aspects, indicating sound sustainability practices. \n"
            "However, both social and governance performances are below industry average, suggesting potential challenges with employee satisfaction, workplace safety, and governance accountability. \n"
            "Investors should pay more attention to the company's social responsibility initiatives to assess potential risks."
        )
        g_advice = (
            "The company's governance performance is below the industry average, suggesting possible issues with board oversight, transparency, or accountability.\n"
            "Investors are advised to closely examine the company's governance practices to evaluate risks associated with management reliability and long-term corporate stability."
        )

    elif e_score <= e_avg and s_score > s_avg and g_score <= g_avg:
        e_advice = (
            "The company shows strong social performance, suggesting effective workforce management and community relations. \n"
            "However, low environmental and governance scores suggest potential environmental risks and governance challenges. \n"
            "Investors are advised to investigate the company's environmental policies and governance practices to mitigate risks."
        )
        g_advice = (
            "The company's governance performance is below the industry average, which may indicate potential weaknesses in transparency, accountability, or board effectiveness.\n"
            "Investors should consider reviewing the company's governance structures and policies to assess potential risks related to management practices and decision-making processes."
        )

    elif e_score <= e_avg and s_score <= s_avg and g_score > g_avg:
        e_advice = (
            "The company's governance is strong, indicating sound management structures. However, environmental and social performances are below industry average, \n"
            "suggesting potential risks in sustainability and employee relations. Investors should carefully evaluate these aspects before proceeding."
        )
        s_advice = (
            "The company's social performance is below the industry average, indicating potential challenges in areas such as employee satisfaction, workplace safety, or community engagement.\n"
            "Investors may need to assess the company's efforts in improving social responsibility to reduce potential risks associated with workforce stability and public perception."
        )

    # 4. 所有指标都低于行业均值
    else:
        e_advice = (
            "The company's environmental performance is below industry standards, suggesting potential issues in areas such as emissions control, energy efficiency, and waste management.\n"
            "Investors should examine the company's policies for emissions reduction, resource optimization, and waste disposal to assess environmental risk."
        )
        s_advice = (
            "The company's social performance is also below the industry average, indicating potential issues with employee satisfaction, workplace safety, or community relations.\n"
            "Investors should investigate the company's approach to employee welfare, training, safety, and inclusion, as poor social performance can affect morale and public perception."
        )
        g_advice = (
            "Governance scores below the industry average suggest potential weaknesses in corporate transparency, board diversity, or accountability practices.\n"
            "Investors are advised to closely evaluate governance structures, including board independence, accountability, and ethical compliance, \n"
            "as poor governance may lead to misconduct and weaken shareholder value."
        )

    # 生成总结和建议
    summary = (
        f"The score of ESG performance is {total_score.round(2)}, and the ranking in the industry is {esg_level}.\n\n"
        f"- {e_text}\n  {e_advice}\n\n"
        f"- {s_text}\n  {s_advice}\n\n"
        f"- {g_text}\n  {g_advice}\n"
    )
    return summary


def generate_summary_regulators():
    # Calculate esg_level
    total_score, e_score, s_score, g_score = get_score()
    total_score = total_score.iloc[0]
    e_score = e_score.iloc[0]
    s_score = s_score.iloc[0]
    g_score = g_score.iloc[0]
    esg_level = determine_esg_level()
    e_avg = 20.81
    s_avg = 18.89
    g_avg = 12.47
    # indicators
    e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
    s_metrics = ['Employee_satisfaction_rate', 'Percentage_of_employees_covered_by_health_insurance', 'Company_donated',
                 "Work_related_injuries"]
    g_metrics = ['Board_independence', 'Women_in_the_management_team', 'Women_on_the_board']
    # average of indicators
    e_avg_metrics = {'Emission_intensities': 0.12, 'Energy_consumption_intensity': 1.96, 'Waste_generated': 339.90,
                     'Water_intensity': 1.84}
    s_avg_metrics = {'Employee_satisfaction_rate': 80, 'Company_donated': 466528.25, "Work_related_injuries": 4.7}
    g_avg_metrics = {'Board_independence': 60, 'Women_in_the_management_team': 42.34, 'Women_on_the_board': 29.68}
    # Default recommendation: for companies with scores above the industry average.
    e_text = f"The score of environmental performance is {e_score.round(2)}."
    e_advice = (
        "The company's environmental performance exceeds the industry average, indicating strong sustainability practices.\n"
        "However, regulatory agencies should monitor changes in environmental policies and standards to ensure the company's practices continue to align with evolving requirements.\n"
        "Attention should be given to the company's ability to adapt its environmental strategies to comply with regulatory updates."
    )

    s_text = f"The score of social performance is {s_score.round(2)}."
    s_advice = (
        "The company's social performance surpasses the industry average, reflecting strong relationships with employees, customers, and communities.\n"
        "Regulatory agencies should encourage the company to maintain these standards, while also monitoring any fluctuations in workforce satisfaction and other social metrics."
    )

    g_text = f"The score of governance performance is {g_score.round(2)}."
    g_advice = (
        "The company's governance performance is above the industry average, reflecting strong management and accountability.\n"
        "Regulatory bodies should continue to ensure that governance practices align with industry standards, focusing on transparency, accountability, and compliance with ethical guidelines."
    )

    # Different scenarios
    # Scenario1: e_score > e_avg and s_score > s_avg and g_score > g_avg
    if e_score > e_avg and s_score > s_avg and g_score > g_avg:
        e_text = f"The score of environmental performance is {e_score.round(2)}, which is higher than the average level of the healthcare industry."
        s_text = f"The score of social performance is {s_score.round(2)}, which is higher than the average level of the healthcare industry."
        g_text = f"The score of governance performance is {g_score.round(2)}, which is higher than the average level of the healthcare industry."

        # Step1: Identify the relatively lowest score among three scores
        lowest_score = min(e_score / 33.53, s_score / 45.90, g_score / 20.57)

        # Situation1
        if lowest_score == e_score / 33.53:
            low_e_metrics = [metric for metric in e_metrics if df[metric].iloc[-1] < e_avg_metrics[metric]]
            if low_e_metrics:
                e_advice = (
                        "Although the company's overall environmental performance is strong, the following environmental indicators are below industry average: "
                        + ", ".join(low_e_metrics) + ".\n"
                                                     "Regulatory agencies should pay close attention to these areas to encourage improvement and ensure the company remains compliant with environmental standards."
                )
            else:
                e_advice = (
                    "The company's environmental performance exceeds the industry average, indicating strong sustainability practices.\n"
                    "However, regulatory agencies should monitor changes in environmental policies to ensure continued alignment with updated standards."
                )

        # Situation2
        if lowest_score == s_score / 45.90:
            low_s_metrics = []

            if df['Employee_satisfaction_rate'].iloc[-1] < s_avg_metrics['Employee_satisfaction_rate']:
                low_s_metrics.append('Employee_satisfaction_rate')

            if df['Company_donated'].iloc[-1] < s_avg_metrics['Company_donated']:
                low_s_metrics.append('Company_donated')

            if df["Work_related_injuries"].iloc[-1] > s_avg_metrics["Work_related_injuries"]:
                low_s_metrics.append("Work_related_injuries")

            if low_s_metrics:
                s_advice = (
                        "Although the company's social performance is generally strong, the following social indicators are below industry average: "
                        + ", ".join(low_s_metrics) + ".\n"
                                                     "Regulatory agencies should monitor these areas to ensure the company addresses any underlying issues and promotes a healthy social environment."
                )
            else:
                s_advice = (
                    "The company's social performance surpasses the industry average, reflecting strong relationships with employees, customers, and communities.\n"
                    "Regulatory agencies should encourage the company to maintain these standards, while monitoring any significant changes."
                )

        # Situation3
        if lowest_score == g_score / 20.57:
            low_g_metrics = [metric for metric in g_metrics if df[metric].iloc[-1] < g_avg_metrics[metric]]

            if low_g_metrics:
                g_advice = (
                        "Although the company's governance score is generally high, the following governance indicators are below industry average: "
                        + ", ".join(low_g_metrics) + ".\n"
                                                     "Regulatory agencies should focus on these governance aspects to promote accountability and prevent potential risks."
                )
            else:
                g_advice = (
                    "The company's governance performance is above industry average, reflecting strong management and accountability.\n"
                    "Regulatory agencies should ensure these practices align with industry standards for sustainable growth and compliance."
                )

    # Other Scenarios
    elif e_score > e_avg and s_score > s_avg and g_score <= g_avg:
        g_advice = (
            "The company demonstrates strong performance in environmental and social aspects, which reflects positively on its sustainability practices.\n"
            "However, governance performance is below industry average. Regulatory agencies should review the company's governance structures to improve transparency, accountability, and decision-making processes."
        )

    elif e_score > e_avg and s_score <= s_avg and g_score > g_avg:
        s_advice = (
            "The company shows strength in environmental and governance aspects, but social performance is below industry average.\n"
            "Regulatory agencies should assess the company's social responsibility initiatives, particularly around workforce satisfaction, to encourage improvement."
        )

    elif e_score <= e_avg and s_score > s_avg and g_score > g_avg:
        e_advice = (
            "The company performs well in social and governance aspects, but its environmental performance is below industry average.\n"
            "Regulatory agencies should focus on the company's environmental practices to ensure alignment with industry standards and encourage sustainable improvements."
        )

    elif e_score > e_avg and s_score <= s_avg and g_score <= g_avg:
        s_advice = (
            "The company has strong environmental practices, but social and governance performances are below industry average.\n"
            "Regulatory agencies should emphasize improvements in social responsibility and governance accountability."
        )
        g_advice = (
            "The company's governance is below industry average, indicating potential issues with oversight and transparency.\n"
            "Regulatory agencies should examine governance practices to mitigate management and compliance risks."
        )

    elif e_score <= e_avg and s_score > s_avg and g_score <= g_avg:
        e_advice = (
            "The company demonstrates good social performance, but its environmental and governance scores are below average.\n"
            "Regulatory agencies should prioritize improvements in environmental practices and governance mechanisms."
        )
        g_advice = (
            "With governance performance below the industry average, regulatory agencies should assess the company’s governance structures to address potential accountability issues."
        )

    elif e_score <= e_avg and s_score <= s_avg and g_score > g_avg:
        e_advice = (
            "The company's governance is strong, but its environmental and social performances are below industry average.\n"
            "Regulatory agencies should consider interventions to improve the company's sustainability and social responsibility efforts."
        )
        s_advice = (
            "The company's social performance falls short of industry standards, indicating areas for improvement in employee and community relations.\n"
            "Regulatory agencies should encourage efforts in these areas to improve social impact."
        )

    # All Scores Below Industry Average
    else:
        e_advice = (
            "The company's environmental performance is below industry standards, suggesting possible issues with emissions, energy efficiency, and waste management.\n"
            "Regulatory agencies should work with the company to address these issues and improve its environmental impact."
        )
        s_advice = (
            "The company's social performance is also below industry average, which may indicate issues with employee satisfaction and community engagement.\n"
            "Regulatory agencies should encourage improvements in social responsibility and workplace conditions."
        )
        g_advice = (
            "The company's governance is below industry standards, highlighting potential weaknesses in transparency, accountability, and ethical compliance.\n"
            "Regulatory agencies should review and promote better governance practices to safeguard shareholder interests."
        )

    # Generate summary and suggestions
    summary = (
        f"The score of ESG performance is {total_score.round(2)}, and the ranking in the industry is {esg_level}.\n\n"
        f"- {e_text}\n  {e_advice}\n\n"
        f"- {s_text}\n  {s_advice}\n\n"
        f"- {g_text}\n  {g_advice}\n"
    )
    return summary


def generate_summary_management():
    # Calculate esg_level
    total_score, e_score, s_score, g_score = get_score()
    total_score = total_score.iloc[0]
    e_score = e_score.iloc[0]
    s_score = s_score.iloc[0]
    g_score = g_score.iloc[0]
    esg_level = determine_esg_level()
    e_avg = 20.81
    s_avg = 18.89
    g_avg = 12.47
    # indicators
    e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
    s_metrics = ['Employee_satisfaction_rate', 'Percentage_of_employees_covered_by_health_insurance', 'Company_donated',
                 "Work_related_injuries"]
    g_metrics = ['Board_independence', 'Women_in_the_management_team', 'Women_on_the_board']
    # average of indicators
    e_avg_metrics = {'Emission_intensities': 0.12, 'Energy_consumption_intensity': 1.96, 'Waste_generated': 339.90,
                     'Water_intensity': 1.84}
    s_avg_metrics = {'Employee_satisfaction_rate': 80, 'Company_donated': 466528.25, "Work_related_injuries": 4.7}
    g_avg_metrics = {'Board_independence': 60, 'Women_in_the_management_team': 42.34, 'Women_on_the_board': 29.68}

    # Default recommendation: for companies with scores above the industry average.
    e_text = f"The score of environmental performance is {e_score.round(2)}."
    e_advice = (
        "The company's environmental performance exceeds the industry average, demonstrating strong sustainability practices.\n"
        "Management should continue to monitor environmental regulations and industry standards to ensure compliance and maintain leadership in environmental responsibility.\n"
        "It's essential to adapt environmental strategies proactively to align with potential regulatory changes."
    )

    s_text = f"The score of social performance is {s_score.round(2)}."
    s_advice = (
        "The company's social performance surpasses the industry average, reflecting positive relations with employees, customers, and communities.\n"
        "Management should focus on maintaining these standards and consider enhancing social initiatives to further strengthen workforce satisfaction and community engagement."
    )

    g_text = f"The score of governance performance is {g_score.round(2)}."
    g_advice = (
        "The company's governance performance is above industry average, indicating strong management and accountability structures.\n"
        "Management should regularly review governance policies to ensure they align with best practices and reinforce transparency and ethical compliance across all levels."
    )

    # Different scenarios
    # Scenario1: e_score > e_avg and s_score > s_avg and g_score > g_avg
    if e_score > e_avg and s_score > s_avg and g_score > g_avg:
        e_text = f"The score of environmental performance is {e_score.round(2)}, which is higher than the average level of the healthcare industry."
        s_text = f"The score of social performance is {s_score.round(2)}, which is higher than the average level of the healthcare industry."
        g_text = f"The score of governance performance is {g_score.round(2)}, which is higher than the average level of the healthcare industry."

        # Step1: Identify the relatively lowest score among three scores
        lowest_score = min(e_score / 33.53, s_score / 45.90, g_score / 20.57)

        # Situation1
        if lowest_score == e_score / 33.53:
            low_e_metrics = [metric for metric in e_metrics if df[metric].iloc[-1] < e_avg_metrics[metric]]
            if low_e_metrics:
                e_advice = (
                        "Although the company's environmental performance is strong overall, the following environmental metrics are below the industry average: "
                        + ", ".join(low_e_metrics) + ".\n"
                                                     "Management should focus on improving these specific areas to ensure comprehensive environmental leadership."
                )
            else:
                e_advice = (
                    "The company's environmental performance exceeds the industry average. Management should continue to monitor environmental policies to ensure ongoing compliance and proactive alignment with regulatory standards."
                )

        # Situation2
        if lowest_score == s_score / 45.90:
            low_s_metrics = []

            if df['Employee_satisfaction_rate'].iloc[-1] < s_avg_metrics['Employee_satisfaction_rate']:
                low_s_metrics.append('Employee_satisfaction_rate')

            if df['Company_donated'].iloc[-1] < s_avg_metrics['Company_donated']:
                low_s_metrics.append('Company_donated')

            if df["Work_related_injuries"].iloc[-1] > s_avg_metrics["Work_related_injuries"]:
                low_s_metrics.append("Work_related_injuries")

            if low_s_metrics:
                s_advice = (
                        "While the company's social performance is strong overall, the following social metrics are below industry average: "
                        + ", ".join(low_s_metrics) + ".\n"
                                                     "Management should address these areas to promote a healthier work environment and stronger community relations."
                )
            else:
                s_advice = (
                    "The company's social performance surpasses the industry average. Management should maintain these standards while proactively monitoring any shifts in employee or community relations."
                )

        # Situation3
        if lowest_score == g_score / 20.57:
            low_g_metrics = [metric for metric in g_metrics if df[metric].iloc[-1] < g_avg_metrics[metric]]

            if low_g_metrics:
                g_advice = (
                        "Although the company's governance is strong overall, the following governance metrics are below industry average: "
                        + ", ".join(low_g_metrics) + ".\n"
                                                     "Management should focus on improving these areas to strengthen transparency and accountability."
                )
            else:
                g_advice = (
                    "The company's governance performance is above industry average. Management should continue to align governance practices with industry best practices to maintain a robust accountability structure."
                )

    # Other Scenarios
    elif e_score > e_avg and s_score > s_avg and g_score <= g_avg:
        g_advice = (
            "The company shows strong environmental and social performance, indicating solid sustainability practices.\n"
            "However, governance performance is below industry average. Management should focus on enhancing governance structures to improve transparency and decision-making processes."
        )

    elif e_score > e_avg and s_score <= s_avg and g_score > g_avg:
        s_advice = (
            "The company demonstrates strength in environmental and governance aspects, but social performance is below industry average.\n"
            "Management should consider bolstering social responsibility efforts, particularly focusing on workforce satisfaction and community engagement."
        )

    elif e_score <= e_avg and s_score > s_avg and g_score > g_avg:
        e_advice = (
            "The company performs well in social and governance aspects, but environmental performance is below industry average.\n"
            "Management should review environmental policies and practices to align with industry standards and drive improvement."
        )

    elif e_score > e_avg and s_score <= s_avg and g_score <= g_avg:
        s_advice = (
            "The company shows strong environmental practices, but social and governance performances are below industry average.\n"
            "Management should prioritize improvements in social responsibility and governance accountability to mitigate potential risks."
        )
        g_advice = (
            "Governance performance is below industry average, suggesting potential gaps in oversight and transparency.\n"
            "Management should reinforce governance practices to improve accountability and strengthen corporate integrity."
        )

    elif e_score <= e_avg and s_score > s_avg and g_score <= g_avg:
        e_advice = (
            "The company demonstrates good social performance, but its environmental and governance scores are below average.\n"
            "Management should enhance environmental policies and governance structures to support long-term resilience and regulatory alignment."
        )
        g_advice = (
            "With governance performance below industry average, management should review and strengthen governance structures to address accountability issues."
        )

    elif e_score <= e_avg and s_score <= s_avg and g_score > g_avg:
        e_advice = (
            "The company's governance is strong, but its environmental and social performances are below industry average.\n"
            "Management should invest in improving sustainability practices and social responsibility to better meet industry standards."
        )
        s_advice = (
            "The company's social performance falls short of industry standards, indicating potential challenges in workforce and community relations.\n"
            "Management should address these areas to enhance social impact and company reputation."
        )

    # All Scores Below Industry Average
    else:
        e_advice = (
            "The company's environmental performance is below industry standards, suggesting potential issues in emissions control, energy efficiency, and waste management.\n"
            "Management should focus on implementing sustainable practices to improve environmental impact and compliance."
        )
        s_advice = (
            "The company's social performance is also below industry average, indicating possible issues with employee satisfaction and community engagement.\n"
            "Management should work to improve social initiatives and strengthen relationships with both employees and the broader community."
        )
        g_advice = (
            "Governance performance is below industry standards, highlighting potential weaknesses in transparency and accountability.\n"
            "Management should strengthen governance practices to improve oversight, accountability, and alignment with ethical standards."
        )

    # Generate summary and suggestions
    summary = (
        f"The score of ESG performance is {total_score.round(2)}, and the ranking in the industry is {esg_level}.\n\n"
        f"- {e_text}\n  {e_advice}\n\n"
        f"- {s_text}\n  {s_advice}\n\n"
        f"- {g_text}\n  {g_advice}\n"
    )
    return summary



