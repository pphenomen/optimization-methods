from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from models.genetic_algorithm import GeneticAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
from dash import html

def register_lr3_callbacks(app):
    @app.callback(
        [Output("rosenbrock-plot", "figure"),
         Output("ga-results", "children")],
        Input("ga-run-button", "n_clicks"),
        [State("ga-pop-size", "value"),
         State("ga-mutation-rate", "value"),
         State("ga-generations", "value"),
         State("function-selector", "value")]
    )
    def run_genetic_algorithm(n_clicks, pop_size, mutation_rate, generations, function_key):
        if n_clicks is None:
            return go.Figure(), ""

        func = FUNCTIONS[function_key]
        ga = GeneticAlgorithm(func=func, pop_size=pop_size, mutation_rate=mutation_rate, generations=generations)
        best_solution, history = ga.run()

        result_text = [
            html.P(f"Лучшее найденное решение: x = {best_solution[0]:.4f}, y = {best_solution[1]:.4f}"),
            html.P(f"Значение функции: f(x, y) = {GeneticAlgorithm.rosenbrock(best_solution[0], best_solution[1]):.4f}")
        ]

        x_vals = np.linspace(-2, 2, 100)
        y_vals = np.linspace(-1, 3, 100)
        X, Y = np.meshgrid(x_vals, y_vals)
        Z = func(X, Y)

        fig = go.Figure(data=[
            go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)
        ])
        
        fig.update_layout(
            title=f"{FUNCTION_NAMES[function_key]}",
            scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='f(x, y)'),
            margin=dict(l=0, r=0, b=0, t=30)
        )

        return fig, result_text
