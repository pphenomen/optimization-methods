from dash import dcc, html
import dash_bootstrap_components as dbc
from views.page_components import (
    create_navbar,
    create_graph,
    create_function_dropdown,
    create_toast,
    create_animation_controls,
    create_results_block
)

layout = dbc.Container([
    create_navbar("Алгоритм роя частиц"),
    dbc.Row([
        dbc.Col(create_graph("pso-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Число частиц"), dbc.Input(id='pso-particles', type='number', value=30)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число итераций"), dbc.Input(id='pso-iterations', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Инерция"), dbc.Input(id='pso-inertia', type='number', value=0.7, step=0.1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Коэфф. когнитивный"), dbc.Input(id='pso-cognitive', type='number', value=1.5, step=0.1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Коэфф. социальный"), dbc.Input(id='pso-social', type='number', value=2.0, step=0.1)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("pso-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id="pso-run-button", color="primary", className="mt-3 w-100"),
                    create_toast("pso-toast"),
                    dcc.Interval(id="pso-interval", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("pso-pause-button", "pso-speed")
                ])
            ]),
            create_results_block("pso-results")
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
