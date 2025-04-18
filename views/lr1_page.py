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
    create_navbar("Метод градиентного спуска с постоянным шагом"),
    dbc.Row([
        dbc.Col(create_graph("3d-plot"), md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Настройки метода", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    dbc.InputGroup([dbc.InputGroupText("X₀"), dbc.Input(id='x0-input', type='number', value=-1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Y₀"), dbc.Input(id='y0-input', type='number', value=-1)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Начальный шаг"), dbc.Input(id='lr-input', type='number', value=0.5, step=0.01)], className='mb-2'),
                    dbc.InputGroup([dbc.InputGroupText("Число итераций"), dbc.Input(id='maxiter-input', type='number', value=100)], className='mb-2'),
                    dbc.InputGroup([create_function_dropdown("function-selector")], className='mb-2 text-dark'),
                    dbc.Button("Запустить", id='run-button', color='primary', className='mt-3 w-100'),
                    create_toast("toast"),
                    dcc.Interval(id='animation-interval', interval=500, n_intervals=0, disabled=True),
                    create_animation_controls('pause-button', 'animation-speed')
                ])
            ]),
            create_results_block("execution-results")
        ], md=4, className="offset-md-2"),
    ])
], fluid=True, className="p-4 bg-dark")
