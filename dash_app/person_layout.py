from dash import dcc, html
import plotly.graph_objects as go
from .plot_functions import get_score,create_gauge,determine_esg_level,create_doughnut_chart,create_doughnut_chart_s,create_doughnut_chart_g,create_bar_chart,generate_summary_investors,generate_summary_management,generate_summary_regulators
from dash import Dash, dcc, html, Input, Output
import pymysql
import pandas as pd

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'esg_database',
    'charset': 'utf8mb4'
}






def fetch_data():
    conn = pymysql.connect(**db_config)
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    sql = "SELECT * FROM ESG_Scores ORDER BY score_id DESC LIMIT 1"
    cursor.execute(sql)

    # 获取结果并转换为 DataFrame
    result = cursor.fetchone()
    conn.close()

    df = pd.DataFrame([result])
    return df

# 定义环形图页面布局
def doughnut_chart_layout():
    df=fetch_data()
    fig_doughnut_chart_e = create_doughnut_chart(df)
    return html.Div(style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'width': '100%',
        'height': '100%',
        'padding': '5px',
        'boxSizing': 'border-box',
        'marginTop': '-60px',
    },children=[
        dcc.Graph(
            id="doughnut-chart3",
            figure=fig_doughnut_chart_e,
            style={'width': '100%', 'height': '400px'}
        )
    ])

# 定义仪表图页面布局
def gauge_chart_layout():
    df = fetch_data()
    fig_gauge = create_gauge(df)
    esg_level = determine_esg_level(df)
    return html.Div(
style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'width': '100%',
        'height': '100%',
        'padding': '5px',
        'boxSizing': 'border-box',
        'marginTop': '25px',
    },
        children=[

        dcc.Graph(
            id="gauge-chart",
            figure=fig_gauge,
            style={'width': '100%', 'height': '250px','overflow': 'hidden'}
        ),
            html.Div(
            f"Industry Rating: {esg_level}",
            style={
                'fontSize': '20px',
                'textAlign': 'center',
                'marginTop': '-5px',
                'color': 'green'
            }
        ),
    ])
def doughnut_chart_layout_s():
    df = fetch_data()
    fig_doughnut_chart_s = create_doughnut_chart_s(df)
    return html.Div(style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'width': '100%',
        'height': '100%',
        'padding': '5px',
        'boxSizing': 'border-box',
        'marginTop': '-60px',
    },children=[
        dcc.Graph(
            id="doughnut-chart2",
            figure=fig_doughnut_chart_s,
            style={'width': '100%', 'height': '400px'}
        )
    ])

def doughnut_chart_layout_g():
    df=fetch_data()
    fig_doughnut_chart_g = create_doughnut_chart_g(df)
    return html.Div(style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'width': '100%',
        'height': '100%',
        'padding': '5px',
        'boxSizing': 'border-box',
        'marginTop': '-60px',
    },children=[
        dcc.Graph(
            id="doughnut-chart3",
            figure=fig_doughnut_chart_g,
            style={'width': '100%', 'height': '400px'}
        )
    ])

def bar_chart_layout():
    df=fetch_data()
    fig_bar_chart = create_bar_chart(df)
    return html.Div([


    # 显示柱状图
    dcc.Graph(id='esg-bar-chart', figure=fig_bar_chart),
])



def drop_selection_layout():


    e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
    s_metrics = ['Employees_covered_by_health_insurance',
                 'Company_donated', 'Avg_training_hours_per_employee', 'Employees_above_50', 'Female_employees',
                 'Employee_satisfaction_rate', 'New_hires_female', 'New_hires_above_50', 'Total_turnover',
                 'Turnover_female',
                 'Turnover_above_50', 'Fatalities', 'High_consequence_injuries',
                 'Work_related_injuries']
    g_metrics = ['Board_independence', 'Women_in_management_team', 'Women_on_board']
    return html.Div([
        # E, S, G dropdowns
        # E dropdown
        html.Div([
            html.Label("Select E Indicators"),
            dcc.Dropdown(
                id="e-dropdown",
                options=[{'label': metric, 'value': metric} for metric in e_metrics],
                multi=True,
                placeholder="Select E indicators"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        # S dropdown
        html.Div([
            html.Label("Select S Indicators"),
            dcc.Dropdown(
                id="s-dropdown",
                options=[{'label': metric, 'value': metric} for metric in s_metrics],
                multi=True,
                placeholder="Select S indicators"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        # G dropdown
        html.Div([
            html.Label("Select G Indicators"),
            dcc.Dropdown(
                id="g-dropdown",
                options=[{'label': metric, 'value': metric} for metric in g_metrics],
                multi=True,
                placeholder="Select G indicators"
            ),
        ], style={'width': '30%', 'display': 'inline-block', 'padding': '10px'}),

        # 输出表格和图表
        html.Div(id="output-table", style={'marginTop': '20px'}),
        dcc.Graph(id="output-graph", style={'height': '400px', 'marginTop': '20px'}),
        dcc.Input(id='dummy-input', type='hidden', value='dummy')  # 隐藏输入用于触发回调
    ])


# 下拉选择表格布局

# 主布局 - 包含URL路径和内容容器
def main_layout():
    return html.Div([
        # 用于监控 URL 变化
        dcc.Location(id='url', refresh=False),  # URL 路由监控组件

        # 内容区域，根据 URL 动态加载不同的页面内容
        html.Div(id='page-content'),  # 动态加载的内容区域

        # 用于输出的静态表格和图表（静态图表不依赖于回调）
        html.Div(id="output-table", style={'marginTop': '20px'}),
        dcc.Graph(id="output-graph", style={'height': '400px', 'marginTop': '20px'})
    ])

def summary_investors_layout():
    df=fetch_data()
    investor_summary = generate_summary_investors(df)
    return html.Div([
        html.H1("ESG Report Summaries and Recommendations", style={'textAlign': 'left', 'marginBottom': '20px'}),
        html.H2("Recommendations for Investors", style={'textAlign': 'left', 'marginTop': '30px'}),
        dcc.Textarea(
            id='investor-summary',
            value=investor_summary,
            style={
                'width': '95%',
                'height': '1000px',
                'margin': 'auto',
                'padding': '10px',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'backgroundColor': '#ffffff',
                'color': '#333333',
                'lineHeight': '1.6',
                'textAlign': 'left',
                'whiteSpace': 'pre-wrap',
                'whiteSpace': 'pre-line'
            },
            readOnly=True
        )
    ])

def summary_management_layout():
    df=fetch_data()
    management_summary = generate_summary_management(df)
    return html.Div([
        html.H1("ESG Report Summaries and Recommendations", style={'textAlign': 'left', 'marginBottom': '20px'}),
        html.H2("Recommendations for Management", style={'textAlign': 'left', 'marginTop': '30px'}),
        dcc.Textarea(
            id='management-summary',
            value=management_summary,
            style={
                'width': '95%',
                'height': '1000px',
                'margin': 'auto',
                'padding': '10px',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'backgroundColor': '#ffffff',
                'color': '#333333',
                'lineHeight': '1.6',
                'textAlign': 'left',
                'whiteSpace': 'pre-wrap',
                'whiteSpace': 'pre-line'
            },
            readOnly=True
        )
    ])
def summary_regulators_layout():
    df=fetch_data()
    regulators_summary = generate_summary_regulators(df)
    return html.Div([
        html.H1("ESG Report Summaries and Recommendations", style={'textAlign': 'left', 'marginBottom': '20px'}),
        html.H2("Recommendations for Regulators", style={'textAlign': 'left', 'marginTop': '30px'}),
        dcc.Textarea(
            id='regulators_summary',
            value=regulators_summary,
            style={
                'width': '95%',
                'height': '1000px',
                'margin': 'auto',
                'padding': '10px',
                'fontFamily': 'Arial',
                'fontSize': '16px',
                'backgroundColor': '#ffffff',
                'color': '#333333',
                'lineHeight': '1.6',
                'textAlign': 'left',
                'whiteSpace': 'pre-wrap',
                'whiteSpace': 'pre-line'
            },
            readOnly=True
        )
    ])