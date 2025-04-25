from dash import html, no_update, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash

from models.bees import BeesAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
from controllers.utils import create_surface_figure, handle_pause, get_pause_button_text

def register_lr5_callbacks(app):
    app.bees_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("bees-plot", "figure"),
         Output("bees-results", "children"),
         Output("bees-run-button", "disabled"),
         Output("bees-interval", "disabled"),
         Output("bees-toast", "is_open"),
         Output("bees-toast", "children")],
        [Input("bees-run-button", "n_clicks"),
         Input("bees-interval", "n_intervals"),
         Input("bees-pause-button", "n_clicks"),
         Input("bees-function-selector", "value")],
        [State("bees-plot", "figure"),
         State("bees-count", "value"),
         State("bees-iters", "value"),
         State("bees-elite", "value"),
         State("bees-selected", "value"),
         State("bees-recruited-elite", "value"),
         State("bees-recruited-selected", "value"),
         State("bees-radius", "value"),
         State("bees-interval", "disabled")]
    )
    def run_bees(n_clicks, n_intervals, pause_clicks, function_key,
                 fig, n_bees, n_iters, n_elite, n_selected_input,
                 n_recruited_elite, n_recruited_selected, radius, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        fig = fig if fig else go.Figure()

        if triggered_id == "bees-pause-button":
            return handle_pause(app.bees_state['running'], interval_disabled)

        if triggered_id == "bees-function-selector":
            if app.bees_state['running']:
                app.bees_state = {
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

        if triggered_id == "bees-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации."

            func = FUNCTIONS[function_key]
            n_selected = max(n_elite + n_selected_input, n_elite)

            optimizer = BeesAlgorithm(
                func=func,
                n_bees=n_bees,
                max_iter=n_iters,
                n_elite=n_elite,
                n_selected=n_selected,
                n_recruited_elite=n_recruited_elite,
                n_recruited_selected=n_recruited_selected,
                bounds=((-5, 5), (-5, 5)),
                radius=radius
            )
            best, history = optimizer.optimize()

            app.bees_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            fig = create_surface_figure(function_key)
            return fig, "Запуск пчелиного алгоритма...", True, False, False, ""

        if triggered_id == "bees-interval" and app.bees_state['running']:
            step = app.bees_state['current_step']
            history = app.bees_state['history']

            if step >= len(history):
                app.bees_state['running'] = False
                best_bee = history[-1]['best']
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best_bee[0]:.4f}, y = {best_bee[1]:.4f}"),
                    html.P(f"Значение функции: {best_bee[2]:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            app.bees_state['current_step'] += 1

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['elite']],
                y=[b[1] for b in step_data['elite']],
                z=[b[2] for b in step_data['elite']],
                mode='markers',
                marker=dict(size=6, color='red'),
                name='Элитные'
            ))

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['selected']],
                y=[b[1] for b in step_data['selected']],
                z=[b[2] for b in step_data['selected']],
                mode='markers',
                marker=dict(size=5, color='cyan'),
                name='Перспективные         '
            ))

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['scouts']],
                y=[b[1] for b in step_data['scouts']],
                z=[b[2] for b in step_data['scouts']],
                mode='markers',
                marker=dict(size=3, color='black'),
                name='Разведчики'
            ))

            fig.add_trace(go.Scatter3d(
                x=[step_data['best'][0]],
                y=[step_data['best'][1]],
                z=[step_data['best'][2]],
                mode='markers',
                marker=dict(size=8, color='gold', symbol='diamond'),
                name='Лучшее'
            ))

            return fig, html.Div([
                html.P(f"Итерация: {step_data['step']}/{len(history)}"),
                html.P(f"Лучшее: ({step_data['best'][0]:.2f}, {step_data['best'][1]:.2f}) -> f = {step_data['best'][2]:.2f}")
            ]), no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("bees-interval", "interval"),
        Input("bees-speed", "value")
    )
    def update_interval(speed):
        return speed

    @app.callback(
        Output("bees-pause-button", "children"),
        Input("bees-interval", "disabled")
    )
    def update_pause_label(disabled):
        return get_pause_button_text(disabled)
