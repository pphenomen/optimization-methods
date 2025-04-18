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
    create_navbar("Иммунный алгоритм"),
    dbc.Row([
        dbc.Col(create_graph("ais-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Итераций"), dbc.Input(id='ais-iters', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Антител"), dbc.Input(id='ais-antibodies', type='number', value=50)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Количество лучших"), dbc.Input(id='ais-best', type='number', value=10)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Случайных антител"), dbc.Input(id='ais-random', type='number', value=10)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Клонов на антитело"), dbc.Input(id='ais-clones', type='number', value=20)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Коэффициент мутации"), dbc.Input(id='ais-mutation', type='number', value=0.2, step=0.01)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("ais-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="ais-run-button", color="success", className="mt-3 w-100"),
                    create_toast("ais-toast"),
                    dcc.Interval(id="ais-interval", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("ais-pause-button", "ais-speed")
                ])
            ]),
            create_results_block("ais-results")
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")