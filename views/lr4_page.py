from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[dbc.Button("Назад", href="/", color="secondary", className="position-absolute", style={"top": "15px", "right": "15px", "zIndex": "1000"})],
        brand="Алгоритм роя частиц (PSO)",
        color="secondary",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="pso-plot", config={"scrollZoom": True}, style={"height": "98%", "width": "130%"})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры PSO", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Число частиц"), dbc.Input(id='pso-particles', type='number', value=30)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число итераций"), dbc.Input(id='pso-iterations', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Инерция"), dbc.Input(id='pso-inertia', type='number', value=0.7, step=0.1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Коэфф. когнитивный"), dbc.Input(id='pso-cognitive', type='number', value=1.5, step=0.1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Коэфф. социальный"), dbc.Input(id='pso-social', type='number', value=2.0, step=0.1)], className='mb-2'),
                    dbc.InputGroup([
                        dbc.InputGroupText("Функция"),
                        dcc.Dropdown(
                            id="function-selector",
                            options=[{"label": FUNCTION_NAMES[k], "value": k} for k in FUNCTION_NAMES],
                            placeholder="Выберите функцию",
                            clearable=False,
                            style={'flex': '1'}
                        )
                    ], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="pso-run-button", color="primary", className="mt-3 w-100"),
                    dbc.Toast("Сначала запустите алгоритм", id="pso-toast", header="Предупреждение", is_open=False,
                              dismissable=True, icon="danger", duration=5000,
                              style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 9999, "width": "15%", "height": "15%", "text-align": "center"}),
                    dcc.Interval(id="pso-interval", interval=500, n_intervals=0, disabled=True),
                    html.Div(id="pso-animation-controls", children=[
                        dbc.Button(id="pso-pause-button", children="Пауза", color="primary", className="mt-2 w-100"),
                        dcc.Slider( id="pso-speed", min=150, max=2000, step=100, value=1000, marks={150: "Быстро", 1000: "Средне", 2000: "Медленно"}, className="mt-2")
                    ])
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id="pso-results", className="p-3 rounded mb-3 bg-secondary text-white", style={"height": "150px", "overflowY": "scroll"})
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
