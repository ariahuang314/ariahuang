

# callbacks.py
# callbacks.py
from dash import Input, Output, html
import pandas as pd
from .person_layout import fetch_data
import plotly.graph_objects as go
import pymysql



def register_callbacks(app):
    @app.callback(
        [Output("output-table", "children"), Output("output-graph", "figure")],
        [Input("e-dropdown", "value"), Input("s-dropdown", "value"), Input("g-dropdown", "value")]
    )
    def update_output(e_selection, s_selection, g_selection):
        df=fetch_data()
        selected_data = {}

        # 选择 E、S、G 的数据
        e_metrics = ['Emission_intensities', 'Energy_consumption_intensity', 'Waste_generated', 'Water_intensity']
        s_metrics = ['Employees_covered_by_health_insurance',
                     'Company_donated', 'Avg_training_hours_per_employee', 'Employees_above_50', 'Female_employees',
                     'Employee_satisfaction_rate', 'New_hires_female', 'New_hires_above_50', 'Total_turnover',
                     'Turnover_female',
                     'Turnover_above_50', 'Fatalities', 'High_consequence_injuries',
                     'Work_related_injuries']
        g_metrics = ['Board_independence', 'Women_in_management_team', 'Women_on_board']

        # 收集选择的数据
        if e_selection:
            for indicator in e_selection:
                if indicator in df.columns:
                    selected_data[indicator] = df[indicator].iloc[-1]
        if s_selection:
            for indicator in s_selection:
                if indicator in df.columns:
                    selected_data[indicator] = df[indicator].iloc[-1]
        if g_selection:
            for indicator in g_selection:
                if indicator in df.columns:
                    selected_data[indicator] = df[indicator].iloc[-1]

        # 如果没有选择任何指标
        if not selected_data:
            return [], go.Figure()  # 返回一个空的图表
        print(selected_data)
        # 创建表格
        table_data = pd.DataFrame(list(selected_data.items()), columns=["Indicator", "Score"])
        table = html.Table([
            html.Thead(html.Tr([html.Th(col) for col in table_data.columns])),
            html.Tbody([
                html.Tr([html.Td(row[col]) for col in table_data.columns]) for _, row in table_data.iterrows()
            ])
        ])

        # 创建柱状图
        fig = go.Figure()
        for indicator, score in selected_data.items():
            color = "lightgreen" if indicator in e_metrics else "lightblue" if indicator in s_metrics else "green"
            fig.add_trace(go.Bar(
                x=[indicator],
                y=[score],
                name=indicator,
                marker=dict(color=color)
            ))

        fig.update_layout(
            title="ESG Indicator Scores",
            yaxis_title="Score",
            xaxis=dict(tickangle=45),
            barmode="group",
            font=dict(size=16)
        )

        return table, fig
