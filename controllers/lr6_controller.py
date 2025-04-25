from dash import html, no_update, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash

from models.immune import ImmuneAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
from controllers.utils import create_surface_figure, handle_pause, get_pause_button_text

def register_lr6_callbacks(app):
    app.ais_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("ais-plot", "figure"),
         Output("ais-results", "children"),
         Output("ais-run-button", "disabled"),
         Output("ais-interval", "disabled"),
         Output("ais-toast", "is_open"),
         Output("ais-toast", "children")],
        [Input("ais-run-button", "n_clicks"),
         Input("ais-interval", "n_intervals"),
         Input("ais-pause-button", "n_clicks"),
         Input("ais-function-selector", "value")],
        [State("ais-plot", "figure"),
         State("ais-iters", "value"),
         State("ais-antibodies", "value"),
         State("ais-best", "value"),
         State("ais-random", "value"),
         State("ais-clones", "value"),
         State("ais-mutation", "value"),
         State("ais-interval", "disabled")]
    )
    def run_ais(n_clicks, n_intervals, pause_clicks, function_key,
                fig, n_iters, n_antibodies, n_best, n_random, n_clones, mutation_rate, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered = ctx.triggered[0]['prop_id'].split('.')[0]
        fig = fig if fig else go.Figure()

        if triggered == "ais-pause-button":
            return handle_pause(app.ais_state['running'], interval_disabled)

        if triggered == "ais-function-selector":
            if app.ais_state["running"]:
                app.ais_state = {
                    'history': [],
                    'current_step': 0,
                    'running': False,
                    'function_key': None
                }
                empty_fig = go.Figure()
                empty_fig.update_layout(scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'), margin=dict(l=0, r=0, b=0, t=30))
                return empty_fig, "", False, True, True, "Работа остановлена из-за смены функции"

            if function_key:
                return create_surface_figure(function_key), no_update, no_update, no_update, False, ""
            else:
                return no_update, no_update, no_update, no_update, False, ""

        if triggered == "ais-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию"

            func = FUNCTIONS[function_key]
            optimizer = ImmuneAlgorithm(
                func=func,
                bounds=((-5, 5), (-5, 5)),
                n_antibodies=n_antibodies,
                n_iterations=n_iters,
                n_best=n_best,
                n_random=n_random,
                n_clones=n_clones,
                mutation_rate=mutation_rate
            )
            best, history = optimizer.optimize()

            app.ais_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            fig = create_surface_figure(function_key)
            return fig, "Запуск иммунного алгоритма...", True, False, False, ""

        if triggered == "ais-interval" and app.ais_state['running']:
            step = app.ais_state['current_step']
            history = app.ais_state['history']

            if step >= len(history):
                app.ais_state['running'] = False
                best_antibody = history[-1]['best']
                score = history[-1]['score']
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best_antibody[0]:.4f}, y = {best_antibody[1]:.4f}"),
                    html.P(f"Значение функции: {score:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            app.ais_state['current_step'] += 1
            func = FUNCTIONS[app.ais_state["function_key"]]

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[a[0] for a in step_data['population']],
                y=[a[1] for a in step_data['population']],
                z=[func(a[0], a[1]) for a in step_data['population']],
                mode='markers',
                marker=dict(size=5, color='black'),
                name='Антитела      '
            ))

            fig.add_trace(go.Scatter3d(
                x=[step_data['best'][0]],
                y=[step_data['best'][1]],
                z=[step_data['score']],
                mode='markers',
                marker=dict(size=6, color='gold', symbol='diamond'),
                name='Лучшее'
            ))

            result_block = html.Div([
                html.P(f"Итерация: {step_data['iteration'] + 1}/{len(history)}"),
                html.P(f"Лучшее: x = {step_data['best'][0]:.4f}, y = {step_data['best'][1]:.4f}"),
                html.P(f"f(x, y) = {step_data['score']:.4f}")
            ])

            return fig, result_block, no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("ais-interval", "interval"),
        Input("ais-speed", "value")
    )
    def update_interval(speed):
        return speed

    @app.callback(
        Output("ais-pause-button", "children"),
        Input("ais-interval", "disabled")
    )
    def update_pause_label(disabled):
        return get_pause_button_text(disabled)
