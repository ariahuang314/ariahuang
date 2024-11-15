# dash_app/__init__.py
from dash import Dash, dcc, html, Input, Output
from .person_layout import main_layout, doughnut_chart_layout, doughnut_chart_layout_s, doughnut_chart_layout_g, gauge_chart_layout, bar_chart_layout, drop_selection_layout,summary_investors_layout,summary_management_layout,summary_regulators_layout
from .plot_functions import  create_gauge
import plotly.graph_objects as go
import pandas as pd
from .callbacks import register_callbacks
import pymysql
import pandas as pd

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456',
    'database': 'esg_database',
    'charset': 'utf8mb4'
}

def create_dash_app(server):
    # 初始化 Dash 应用，并与 Flask 服务器集成
    app = Dash(__name__, server=server, url_base_pathname='/dash/', suppress_callback_exceptions=True)

    # 主布局，包含 Location 组件以监控 URL 的变化
    app.layout = main_layout()
    register_callbacks(app)

    # 注册应用的回调


    # 页面内容更新回调
    @app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
    def display_page(pathname):

        if pathname == "/dash/doughnut_chart_e":
            return doughnut_chart_layout()
        elif pathname == "/dash/doughnut_chart_s":
            return doughnut_chart_layout_s()
        elif pathname == "/dash/doughnut_chart_g":
            return doughnut_chart_layout_g()
        elif pathname == "/dash/gauge":
            return gauge_chart_layout()
        elif pathname == "/dash/bar_chart":

            return bar_chart_layout()
        elif pathname == "/dash/drop_selection":

            return drop_selection_layout()
        elif pathname == "/dash/investor_summary":

            return summary_investors_layout()
        elif pathname == "/dash/management_summary":

            return summary_management_layout()
        elif pathname == "/dash/regulators_summary":

            return summary_regulators_layout()
        else:
            return html.Div("404 Page Not Found")

    return app