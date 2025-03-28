from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[dbc.Button("Назад", href="/", color="secondary", className="position-absolute", style={"top": "15px", "right": "15px", "zIndex": "1000"})],
        brand="Метод градиентного спуска с постоянным шагом",
        color="secondary",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([ 
            dcc.Graph(id='3d-plot', config={'scrollZoom': True}, style={'height': '98%', 'width': '130%'})
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
                            placeholder="Выберите функцию",
                            clearable=False,
                            style = {'flex' : '1'}
                        )
                    ], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id='run-button', color='primary', className='mt-3 w-100'),
                    dbc.Toast("Сначала запустите алгоритм", id="toast", header="Предупреждение", is_open=False,
                              dismissable=True, icon="danger", duration=5000,
                              style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 9999, "width": "15%", "height": "15%", "text-align": "center"}),
                    dcc.Interval(id='animation-interval', interval=500, n_intervals=0, disabled=True),
                    html.Div(id='animation-controls',  children=[
                        dbc.Button(id='pause-button', children="Пауза", color='primary', className='mt-2 w-100'),
                        dcc.Slider(id='animation-speed', min=150, max=2000, step=100, value=1000, marks={150: 'Быстро', 1000: 'Средне', 2000: 'Медленно'}, className='mt-2')
                        ]),
                    ])
                ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id='execution-results', className='p-3 rounded mb-3 bg-secondary text-white', style={'height': '150px', 'overflowY': 'scroll'})
        ], md=4, className="offset-md-2"),
    ]),
], fluid=True, className="p-4 bg-dark")