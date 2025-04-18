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
    create_navbar("Бактериальная оптимизация"),
    dbc.Row([
        dbc.Col(create_graph("bfoa-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Итерации"), dbc.Input(id='bfoa-iters', type='number', value=150)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Бактерий"), dbc.Input(id='bfoa-bacteria', type='number', value=40)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Шаг плавания"), dbc.Input(id='bfoa-swim', type='number', value=6)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Шаг ликвидации"), dbc.Input(id='bfoa-elimination', type='number', value=15)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число ликвидируемых"), dbc.Input(id='bfoa-eliminated', type='number', value=25)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("bfoa-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="bfoa-run-button", color="success", className="mt-3 w-100"),
                    create_toast("bfoa-toast"),
                    dcc.Interval(id="bfoa-interval", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("bfoa-pause-button", "bfoa-speed")
                ])
            ]),
            create_results_block("bfoa-results") 
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
