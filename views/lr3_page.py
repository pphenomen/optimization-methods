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
    create_navbar("Генетический алгоритм"),
    dbc.Row([
        dbc.Col(create_graph("rosenbrock-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Параметры алгоритма", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("Размер популяции"), dbc.Input(id='ga-pop-size', type='number', value=50)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Ставка мутации"), dbc.Input(id='ga-mutation-rate', type='number', value=0.1, step=0.01)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число поколений"), dbc.Input(id='ga-generations', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("ga-function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id='ga-run-button', color='success', className='mt-3 w-100'),
                    create_toast("ga-toast"),
                    dcc.Interval(id='ga-interval', interval=500, n_intervals=0, disabled=True),
                    create_animation_controls('ga-pause-button', 'ga-animation-speed')
                ])
            ]),
            create_results_block("ga-results")
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
