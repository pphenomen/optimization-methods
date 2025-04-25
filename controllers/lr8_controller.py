from dash import html, no_update, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash

from models.functions import FUNCTIONS, FUNCTION_NAMES
from models.genetic import GeneticAlgorithm
from models.bees import BeesAlgorithm
from models.hybrid import HybridOptimization
from controllers.utils import create_surface_figure, handle_pause, get_pause_button_text

def register_lr8_callbacks(app):
    app.hybrid_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("hybrid-plot", "figure"),
         Output("hybrid-results", "children"),
         Output("hybrid-run-button", "disabled"),
         Output("hybrid-interval", "disabled"),
         Output("hybrid-toast", "is_open"),
         Output("hybrid-toast", "children")],
        [Input("hybrid-run-button", "n_clicks"),
         Input("hybrid-interval", "n_intervals"),
         Input("hybrid-pause-button", "n_clicks"),
         Input("hybrid-function-selector", "value")],
        [State("hybrid-plot", "figure"),
         State("hybrid-generations", "value"),
         State("hybrid-pop-size", "value"),
         State("hybrid-mutation-rate", "value"),
         State("hybrid-radius", "value"),
         State("hybrid-interval", "disabled")]
    )
    def run_hybrid(n_clicks, n_intervals, pause_clicks, function_key,
                   fig, generations, pop_size, mutation_rate, radius, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered = ctx.triggered[0]['prop_id'].split('.')[0]
        fig = fig if fig else go.Figure()

        if triggered == "hybrid-pause-button":
            return handle_pause(app.hybrid_state['running'], interval_disabled)

        if triggered == "hybrid-function-selector":
            if app.hybrid_state["running"]:
                app.hybrid_state = {
                    'history': [],
                    'current_step': 0,
                    'running': False,
                    'function_key': None
                }
                empty_fig = go.Figure()
                empty_fig.update_layout(scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'), margin=dict(l=0, r=0, b=0, t=30))
                return empty_fig, "", False, True, True, "Работа алгоритма остановлена из-за смены функции"

            if function_key:
                return create_surface_figure(function_key), no_update, no_update, no_update, False, ""
            else:
                return no_update, no_update, no_update, no_update, False, ""

        if triggered == "hybrid-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию"

            func = FUNCTIONS[function_key]

            ga = GeneticAlgorithm(func, generations=generations, pop_size=pop_size, mutation_rate=mutation_rate)
            ba = BeesAlgorithm(func, n_bees=pop_size, max_iter=generations, radius=radius)

            optimizer = HybridOptimization(func, generations=generations)
            optimizer.genetic = ga
            optimizer.bees = ba

            _, history = optimizer.run()

            app.hybrid_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            fig = create_surface_figure(function_key)
            return fig, "Запуск гибридного алгоритма...", True, False, False, ""

        if triggered == "hybrid-interval" and app.hybrid_state['running']:
            step = app.hybrid_state['current_step']
            history = app.hybrid_state['history']

            if step >= len(history):
                app.hybrid_state['running'] = False
                best = history[-1]
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best['best'][0]:.4f}, y = {best['best'][1]:.4f}"),
                    html.P(f"Значение функции f(x, y): {best['score']:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            population = step_data["population"]
            best = step_data["best"]
            score = step_data["score"]
            func = FUNCTIONS[app.hybrid_state["function_key"]]

            app.hybrid_state['current_step'] += 1

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=population[:, 0],
                y=population[:, 1],
                z=[func(x, y) for x, y in population],
                mode='markers',
                marker=dict(size=5, color='black'),
                name='Популяция         '
            ))

            fig.add_trace(go.Scatter3d(
                x=[best[0]], y=[best[1]], z=[score],
                mode='markers',
                marker=dict(size=6, color='gold', symbol='diamond'),
                name='Лучшая'
            ))

            result_block = html.Div([
                html.P(f"Итерация: {step + 1}/{len(history)}"),
                html.P(f"x = {best[0]:.4f}, y = {best[1]:.4f}"),
                html.P(f"f(x, y) = {score:.4f}")
            ])

            return fig, result_block, no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("hybrid-interval", "interval"),
        Input("hybrid-speed", "value")
    )
    def update_interval(speed):
        return speed

    @app.callback(
        Output("hybrid-pause-button", "children"),
        Input("hybrid-interval", "disabled")
    )
    def update_pause_label(disabled):
        return get_pause_button_text(disabled)
