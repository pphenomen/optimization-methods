from dash import dcc, html
import dash_bootstrap_components as dbc
from views.page_components import (
    create_navbar,
    create_graph,
    create_function_dropdown,
    create_toast,
    create_animation_controls,
    create_results_block,
    create_log_modal
)

layout = dbc.Container([
    create_navbar("Пчелиный алгоритм", color="warning"),
    dbc.Row([
        dbc.Col(create_graph("bees-plot"), md=6),
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
                    dbc.InputGroup([create_function_dropdown("bees-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="bees-run-button", color="success", className="mt-3 w-100"),
                    create_toast("bees-toast", message="Сначала выберите функцию"),
                    dcc.Interval(id="bees-interval", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("bees-pause-button", "bees-speed")
                ])
            ]),
            create_results_block("bees-results"),
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
