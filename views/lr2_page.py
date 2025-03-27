from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[dbc.Button("Назад", href="/", color="secondary", className="ms-3")],
        brand="Решение задачи квадратичного программирования",
        color="secondary",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id="qp-graph",
                config={"scrollZoom": True},
                style={'height': '550px', 'width': '950px'},
                figure={
                    'data': [],
                    'layout': {
                        'scene': {
                            'xaxis': {'title': 'x1'},
                            'yaxis': {'title': 'x2'},
                            'zaxis': {'title': 'f(x1,x2)'}
                        },
                        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0}
                    }
                }
            )
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Условие задачи", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    html.Div([
                        html.P("Минимизировать:", className="mb-1 text-white"),
                        html.Pre("f(x) = 2x₁² + 3x₂² + 4x₁x₂ - 6x₁ - 3x₂", className="text-white"),
                        html.P("при условиях:", className="mb-1 text-white"),
                        html.Pre("x₁ + x₂ ≤ 1\n2x₁ + 3x₂ ≤ 4\nx₁ ≥ 0, x₂ ≥ 0", className="text-white")
                    ], className="mb-3"),
                    dbc.Button("Запустить", id="qp-run-button", color="primary", className="w-100", n_clicks=0),
                    dcc.Interval(id="interval-component", interval=500, n_intervals=0, disabled=True),
                    html.Div(id="qp-animation-controls", children=[
                        dbc.Button("Пауза", id="qp-pause-button", color="primary", className="mt-2 w-100"),
                        dcc.Slider(
                            id="qp-animation-speed",
                            min=100,
                            max=2000,
                            step=100,
                            value=500,
                            marks={100: 'Быстро', 1000: 'Средне', 2000: 'Медленно'},
                            className="mt-2"
                        )
                    ]),
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(
                id="qp-results",
                className="p-3 rounded mb-3 bg-secondary text-white",
                style={'height': '150px', 'overflowY': 'scroll'},
                children="Нажмите 'Запустить' для начала решения"
            ),
        ], md=4, className="offset-md-2"),
    ]),
    dcc.Interval(
        id="interval-component",
        interval=500,
        n_intervals=0,
        disabled=True
    )
], fluid=True, className="p-4 bg-dark")
