from dash import dcc, html
import dash_bootstrap_components as dbc
from views.page_components import (
    create_navbar,
    create_graph,
    create_toast,
    create_animation_controls,
    create_results_block
)

layout = dbc.Container([
    create_navbar("Решение задачи квадратичного программирования"),
    dbc.Row([
        dbc.Col([
            create_graph("qp-graph")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Условие задачи", className="text-center bg-secondary text-white"),
                dbc.CardBody([
                    html.Div([
                        html.P("Минимизировать:", className="mb-1 text-white"),
                        html.Pre("f(x) = 2x₁² + 3x₂² + 4x₁x₂ - 6x₁ - 3x₂", className="text-white"),
                        html.P("при условиях:", className="mb-1 text-white"),
                        html.Pre("x₁ + x₂ ≤ 1\n2x₁ + 3x₂ ≤ 4\nx₁ ≥ 0, x₂ ≥ 0", className="text-white")
                    ], className="mb-3"),
                    dbc.Button("Запустить", id="qp-run-button", color="primary", className="w-100"),
                    create_toast("qp-toast"),
                    dcc.Interval(id="interval-component", interval=500, n_intervals=0, disabled=True),
                    create_animation_controls("qp-pause-button", "qp-animation-speed")
                ])
            ]),
            create_results_block("qp-results")
        ], md=4, className="offset-md-2")
    ])
], fluid=True, className="p-4 bg-dark")
