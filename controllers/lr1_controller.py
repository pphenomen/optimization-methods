from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from models.gradient_descent import GradientDescent
from models.functions import FUNCTIONS, FUNCTION_NAMES
from dash import html

def register_lr1_callbacks(app):
    @app.callback(
        [Output("3d-plot", "figure"),
         Output("execution-results", "children")],
        Input("run-button", "n_clicks"),
        [State("x0-input", "value"),
         State("y0-input", "value"),
         State("lr-input", "value"),
         State("maxiter-input", "value"),
         State("function-selector", "value")]
    )
    def update_lr1_plot(n_clicks, x0, y0, lr, max_iter, function_key):
        if n_clicks is None:
            return go.Figure(), ""

        func = FUNCTIONS[function_key]

        gd = GradientDescent(func=func, x0=x0, y0=y0, learning_rate=lr, max_iter=max_iter)
        history, converged, message = gd.run()

        result_text = [
            html.P(message, className="text-white"),
            html.Ul([
                html.Li(f"Итерация {step['iteration']}: x = {step['x']:.4f}, y = {step['y']:.4f}, f(x, y) = {step['f_value']:.4f}")
                for step in history
            ])
        ]

        x_vals = np.linspace(-5, 5, 50)
        y_vals = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func(X, Y)

        trajectory_x = [step["x"] for step in history]
        trajectory_y = [step["y"] for step in history]
        trajectory_z = [step["f_value"] for step in history]

        fig = go.Figure(data=[
            go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8),
            go.Scatter3d(x=trajectory_x, y=trajectory_y, z=trajectory_z,
                         mode='lines+markers', marker=dict(size=5, color='red'),
                         line=dict(color='red', width=2))
        ])

        fig.update_layout(
            title=f"{FUNCTION_NAMES[function_key]}",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='f(x, y)'),
            margin=dict(l=0, r=0, b=0, t=30)
        )

        return fig, result_text
