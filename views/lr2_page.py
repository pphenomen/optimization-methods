from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[dbc.Button("Назад", href="/", color="secondary", className="ms-3")],
        brand="Решение задач квадратичного программирования",
        color="secondary",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="qp-graph", config={"scrollZoom": True}, style={'height': '550px', 'width': '950px'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры задачи", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.Label("Выберите задачу:", className="text-white"),
                    dcc.Dropdown(
                        id="problem-selector",
                        options=[
                            {"label": "Задача 1 (Минимизация)", "value": "problem_1"},
                            {"label": "Задача 2 (Максимизация)", "value": "problem_2"}
                        ],
                        value="problem_1",
                        clearable=False,
                        className="mb-3 text-dark"
                    ),
                    dbc.Button("Запустить", id="qp-run-button", color="primary", className="w-100"),
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id="qp-results", className="p-3 rounded mb-3 bg-secondary text-white",
                     style={'height': '150px', 'overflowY': 'scroll'}),
        ], md=4, className="offset-md-2"),
    ]),
    dcc.Interval(id="interval-component", interval=500, n_intervals=0, disabled=True)
], fluid=True, className="p-4 bg-dark")