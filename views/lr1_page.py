from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[
            dbc.Button("Назад", href="/", color="secondary", className="ms-3")
        ],
        brand="Метод градиентного спуска с постоянным шагом",
        color="secondary",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([ 
            dcc.Graph(id='3d-plot', config={'scrollZoom': True}, style={'height': '550px', 'width': '950px'})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Настройки метода", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("X₀"), dbc.Input(id='x0-input', type='number', value=-1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Y₀"), dbc.Input(id='y0-input', type='number', value=-1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Начальный шаг"), dbc.Input(id='lr-input', type='number', value=0.5, step=0.01)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число итераций"), dbc.Input(id='maxiter-input', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([
                        dbc.InputGroupText("Выбор функции"),
                        dcc.Dropdown(
                            id='function-selector',
                            options=[{'label': FUNCTION_NAMES[key], 'value': key} for key in FUNCTION_NAMES.keys()],
                            value='sphere',
                            clearable=False,
                            style = {'flex' : '1'}
                        )
                    ], className='mb-2 text-dark'),
                    dbc.Button("Выполнить", id='run-button', color='primary', className='mt-3 w-100')
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id='execution-results', className='p-3 rounded mb-3 bg-secondary text-white', style={'height': '150px', 'overflowY': 'scroll'})
        ], md=4, className="offset-md-2"),
    ]),
], fluid=True, className="p-4 bg-dark")