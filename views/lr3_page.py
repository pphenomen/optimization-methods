from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

layout = dbc.Container([
    dbc.NavbarSimple(children=[dbc.Button("Назад", href="/", color="secondary", className="ms-3")],
        brand="Генетический алгоритм",
        color="secondary", dark=True, brand_style={"fontSize": "26px", "fontWeight": "bold"}, className="bg-dark"),
    dbc.Row([
        dbc.Col([dcc.Graph(id="rosenbrock-plot", config={"scrollZoom": True}, style={'height': '550px', 'width': '950px'})], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Размер популяции"), dbc.Input(id='ga-pop-size', type='number', value=50)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Ставка мутации"), dbc.Input(id='ga-mutation-rate', type='number', value=0.1, step=0.01)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число поколений"), dbc.Input(id='ga-generations', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([
                        dbc.InputGroupText("Выбор функции"),
                        dcc.Dropdown(
                            id='function-selector',
                            options=[{'label': FUNCTION_NAMES[key], 'value': key} for key in FUNCTION_NAMES.keys()],
                            value="rosenbrock",
                            clearable=False,
                            style = {'flex' : '1'}
                        )
                    ], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id='ga-run-button', color='primary', className='mt-3 w-100')
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id='ga-results', className='p-3 rounded mb-3 bg-secondary text-white', style={'height': '150px', 'overflowY': 'scroll'})
        ], md=4, className="offset-md-2"),
    ]),
], fluid=True, className="p-4 bg-dark")
