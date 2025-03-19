from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from models.quadratic_programming import QuadraticProgrammingSolver
from dash import html

def register_lr2_callbacks(app):
    @app.callback(
        [Output("qp-graph", "figure"), Output("qp-results", "children")],
        Input("qp-run-button", "n_clicks"),
        [State("problem-selector", "value")]
    )
    def run_qp(n_clicks, problem_key):
        if not n_clicks:
            return go.Figure(), ""

        if problem_key == "problem_1":
            Q = [[2, 2], [2, 3]]
            c = [-6, -3]
            A = [[1, 1], [2, 3]]
            b = [1, 4]
        else:
            Q = [[0, 0], [0, -2]]
            c = [1, 2]
            A = [[3, 2], [1, 2]]
            b = [6, 4]

        solver = QuadraticProgrammingSolver(Q, c, A, b)
        solution, _, _, _ = solver.solve()  

        result_text = html.P(f"Оптимальное решение: x = {solution[0]:.4f}, y = {solution[1]:.4f}")

        X, Y = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
        func = lambda x, y: 0.5 * (Q[0][0] * x**2 + Q[1][1] * y**2 + 2 * Q[0][1] * x * y) + c[0] * x + c[1] * y
        Z = func(X, Y)

        fig = go.Figure([
            go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8),
            go.Scatter3d(x=[solution[0]], y=[solution[1]], z=[func(solution[0], solution[1])],
                         mode="markers", marker=dict(size=5, color="red"))
        ])

        return fig, result_text
