from dash import dcc, html
from flask import session
from .plot_functions import create_gauge,determine_esg_level,create_doughnut_chart

person_fig_gauge=create_gauge()
person_esg_level=determine_esg_level()
fig_doughnut_chart_e=create_doughnut_chart()



person_layout_gauge = html.Div(
style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center',
        'width': '100%',
        'height': '100%',
        'padding': '5px',
        'boxSizing': 'border-box',
        'marginTop': '-25px',
    },
children=[
        dcc.Graph(
            id='person-gauge',
            figure=person_fig_gauge,  # 示例分数
            style={'width': '100%', 'height': '250px'}  # 限制仪表图高度
        ),
        html.Div(
            f"Industry Rating: {person_esg_level}",
            style={
                'fontSize': '20px',
                'textAlign': 'center',
                'marginTop': '-5px',
                'color': 'green'
            }
        ),
    ]
)

person_layout_doughnut_chart_e= html.Div([

    # 环状图显示 E Score
    dcc.Graph(id = "e-score-chart", figure = create_doughnut_chart()),
])