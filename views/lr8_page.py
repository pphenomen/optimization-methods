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
    create_navbar("Гибридный алгоритм (Пчелиный + Генетический)"),
    dbc.Row([
        dbc.Col(create_graph("hybrid-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Итерации"), dbc.Input(id='hybrid-generations', type='number', value=50, min=10)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Популяция"), dbc.Input(id='hybrid-pop-size', type='number', value=40, min=10)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Мутация"), dbc.Input(id='hybrid-mutation-rate', type='number', value=0.08, min=0.01, max=0.5, step=0.01)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Радиус пчёл"), dbc.Input(id='hybrid-radius', type='number', value=0.05, min=0.01, max=1.0, step=0.01)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("hybrid-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="hybrid-run-button", color="success", className="mt-3 w-100"),
                    create_toast("hybrid-toast"),
                    dcc.Interval(id="hybrid-interval", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("hybrid-pause-button", "hybrid-speed")
                ])
            ]),
            create_results_block("hybrid-results")
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
