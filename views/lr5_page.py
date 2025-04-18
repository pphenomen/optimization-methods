from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

layout = dbc.Container([
    dbc.NavbarSimple(
        children=[dbc.Button("Назад", href="/", color="secondary", className="position-absolute", style={"top": "15px", "right": "15px", "zIndex": "1000"})],
        brand="Пчелиный алгоритм",
        color="warning",
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="bees-plot", config={"scrollZoom": True}, style={"height": "98%", "width": "130%"})
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Итераций"), dbc.Input(id='bees-iters', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Разведчики"), dbc.Input(id='bees-count', type='number', value=20)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Пчел в перспективном участке"), dbc.Input(id='bees-recruited-selected', type='number', value=10)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Пчел в лучшем участке"), dbc.Input(id='bees-recruited-elite', type='number', value=20)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Перспективных участков"), dbc.Input(id='bees-selected', type='number', value=3)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Лучших участков"), dbc.Input(id='bees-elite', type='number', value=1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Размер участков"), dbc.Input(id='bees-radius', type='number', value=0.5, step=0.1)], className='mb-2'),
                    dbc.InputGroup([
                        dbc.InputGroupText("Функция"),
                        dcc.Dropdown(
                            id="bees-function-selector",
                            options=[{"label": FUNCTION_NAMES[k], "value": k} for k in FUNCTION_NAMES],
                            placeholder="Выберите функцию",
                            clearable=False,
                            style={'flex': '1'}
                        )
                    ], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="bees-run-button", color="success", className="mt-3 w-100"),
                    dbc.Toast("Сначала выберите функцию", id="bees-toast", header="Предупреждение", is_open=False,
                              dismissable=True, icon="danger", duration=5000,
                              style={"position": "fixed", "top": "50%", "left": "50%", "transform": "translate(-50%, -50%)", "zIndex": 9999, "width": "15%", "height": "15%", "text-align": "center"}),
                    dcc.Interval(id="bees-interval", interval=500, n_intervals=0, disabled=True),
                    html.Div(id="bees-animation-controls", children=[
                        dbc.Button(id="bees-pause-button", children="Пауза", color="primary", className="mt-2 w-100"),
                        dcc.Slider(id="bees-speed", min=150, max=2000, step=100, value=1000,
                                   marks={150: "Быстро", 1000: "Средне", 2000: "Медленно"}, className="mt-2")
                    ])
                ])
            ]),
            html.H4("Выполнение и результаты", className="mt-2 text-white"),
            html.Div(id="bees-results", className="p-3 rounded mb-3 bg-secondary text-white", style={"height": "150px", "overflowY": "scroll"}),
            html.Div([
                dbc.Button("Открыть логи", id="open-log-modal", color="primary", size="sm", className="me-2 flex-fill"),
                dbc.Button("Очистить логи", id="clear-log", color="danger", size="sm", className="flex-fill"),
            ], className="d-flex mt-2"),
            
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Подробные логи")),
                dbc.ModalBody(html.Div(id="bees-modal-results", className="p-3 rounded mb-3 bg-secondary text-white", style={"maxHeight": "70vh", "overflowY": "auto"})),
                dbc.ModalFooter(dbc.Button("Закрыть", id="close-log-modal", className="ms-auto", n_clicks=0))
                ], backdrop=False, id="log-modal", is_open=False, size="xl", scrollable=True)
                            
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
