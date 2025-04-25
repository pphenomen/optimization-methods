from dash import html, no_update, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash

from models.pso import ParticleSwarmOptimizer
from models.functions import FUNCTIONS, FUNCTION_NAMES
from controllers.utils import create_surface_figure, handle_pause, get_pause_button_text

def register_lr4_callbacks(app):
    app.pso_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("pso-plot", "figure"),
         Output("pso-results", "children"),
         Output("pso-run-button", "disabled"),
         Output("pso-interval", "disabled"),
         Output("pso-toast", "is_open"),
         Output("pso-toast", "children")],
        [Input("pso-run-button", "n_clicks"),
         Input("pso-interval", "n_intervals"),
         Input("pso-pause-button", "n_clicks"),
         Input("pso-function-selector", "value")],
        [State("pso-plot", "figure"),
         State("pso-particles", "value"),
         State("pso-iterations", "value"),
         State("pso-inertia", "value"),
         State("pso-cognitive", "value"),
         State("pso-social", "value"),
         State("pso-interval", "disabled")]
    )
    def run_pso(n_clicks, n_intervals, pause_clicks, function_key,
                fig, n_particles, n_iters, inertia, cognitive, social, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        fig = fig if fig else go.Figure()

        if triggered_id == "pso-pause-button":
            return handle_pause(app.pso_state['running'], interval_disabled)

        if triggered_id == "pso-function-selector":
            if app.pso_state['running']:
                app.pso_state = {
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

        if triggered_id == "pso-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации."

            func = FUNCTIONS[function_key]
            optimizer = ParticleSwarmOptimizer(func=func, num_particles=n_particles, iterations=n_iters,
                                               inertia=inertia, cognitive=cognitive, social=social)
            best_pos, best_val, history = optimizer.optimize()

            app.pso_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            fig = create_surface_figure(function_key)
            return fig, "Запуск оптимизации роя частиц...", True, False, False, ""

        if triggered_id == "pso-interval" and app.pso_state['running']:
            step = app.pso_state['current_step']
            history = app.pso_state['history']

            if step >= len(history):
                app.pso_state['running'] = False
                pos, val = history[-1]
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {pos[0]:.4f}, y = {pos[1]:.4f}"),
                    html.P(f"Значение функции: {val:.4f}")
                ]), False, True, False, ""

            pos, val = history[step]
            app.pso_state['current_step'] += 1

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            xs = [h[0][0] for h in history[:step+1]]
            ys = [h[0][1] for h in history[:step+1]]
            zs = [h[1] for h in history[:step+1]]

            fig.add_trace(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode='lines+markers',
                marker=dict(size=4, color='red'),
                line=dict(color='red', width=2),
                name='Траектория'
            ))

            return fig, html.Div([
                html.P(f"Итерация: {step+1}/{len(history)}"),
                html.P(f"x = {pos[0]:.4f}, y = {pos[1]:.4f}, f(x, y) = {val:.4f}")
            ]), no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("pso-interval", "interval"),
        Input("pso-speed", "value")
    )
    def update_interval(speed):
        return speed

    @app.callback(
        Output("pso-pause-button", "children"),
        Input("pso-interval", "disabled")
    )
    def update_pause_button_text(disabled):
        return get_pause_button_text(disabled)
