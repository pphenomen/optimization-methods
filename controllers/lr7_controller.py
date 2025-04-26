from dash import html, no_update, callback_context
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import dash

from models.bacterial import BacterialOptimization
from models.functions import FUNCTIONS, FUNCTION_NAMES
from controllers.utils import create_surface_figure, handle_pause, get_pause_button_text

def register_lr7_callbacks(app):
    app.bfoa_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("bfoa-plot", "figure"),
         Output("bfoa-results", "children"),
         Output("bfoa-run-button", "disabled"),
         Output("bfoa-interval", "disabled"),
         Output("bfoa-toast", "is_open"),
         Output("bfoa-toast", "children")],
        [Input("bfoa-run-button", "n_clicks"),
         Input("bfoa-interval", "n_intervals"),
         Input("bfoa-pause-button", "n_clicks"),
         Input("bfoa-function-selector", "value")],
        [State("bfoa-plot", "figure"),
         State("bfoa-iters", "value"),
         State("bfoa-bacteria", "value"),
         State("bfoa-swim", "value"),
         State("bfoa-elimination", "value"),
         State("bfoa-eliminated", "value"),
         State("bfoa-interval", "disabled")]
    )
    def run_bfoa(n_clicks, n_intervals, pause_clicks, function_key,
                 fig, n_iters, n_bacteria, swim_step, elimination_step, n_eliminated, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered = ctx.triggered[0]['prop_id'].split('.')[0]
        fig = fig if fig else go.Figure()

        if triggered == "bfoa-pause-button":
            return handle_pause(app.bfoa_state['running'], interval_disabled)

        if triggered == "bfoa-function-selector":
            if app.bfoa_state["running"]:
                app.bfoa_state = {
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

        if triggered == "bfoa-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию"

            func = FUNCTIONS[function_key]
            optimizer = BacterialOptimization(
                func=func,
                bounds=((-5, 5), (-5, 5)),
                n_bacteria=n_bacteria,
                n_iterations=n_iters,
                step_size=0.1,
                mutation_rate=elimination_step / 100 if elimination_step else 0.1,
                attraction=0.5,
                repulsion=0.5
            )
            best, history = optimizer.optimize()

            app.bfoa_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            fig = create_surface_figure(function_key)
            return fig, "Запуск бактериальной оптимизации...", True, False, False, ""

        if triggered == "bfoa-interval" and app.bfoa_state['running']:
            step = app.bfoa_state['current_step']
            history = app.bfoa_state['history']
            func = FUNCTIONS[app.bfoa_state['function_key']]

            if step >= len(history):
                app.bfoa_state['running'] = False
                best = history[-1]['best_solution']
                score = history[-1]['best_score']
                displayed = 0.0 if abs(score) <= 1e-6 else score
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best[0]:.6f}, y = {best[1]:.6f}"),
                    html.P(f"Значение функции: {displayed:.6f}"),
                    html.P(f"Алгоритм выполнил все {len(history)} итераций.")
                ]), False, True, False, ""

            step_data = history[step]
            app.bfoa_state['current_step'] += 1

            # Автоостановка, если достигли нуля
            if abs(step_data['best_score']) <= 1e-6:
                app.bfoa_state['running'] = False
                best = step_data['best_solution']
                displayed = 0.0
                return fig, html.Div([
                    html.P(f"Решение найдено на {step_data['iteration'] + 1}-й итерации!"),
                    html.P(f"Координаты: x = {best[0]:.6f}, y = {best[1]:.6f}"),
                    html.P(f"Значение функции: {displayed:.6f}")
                ]), False, True, False, ""

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[p[0] for p in step_data['population']],
                y=[p[1] for p in step_data['population']],
                z=[func(p[0], p[1]) for p in step_data['population']],
                mode='markers',
                marker=dict(size=5, color='black'),
                name='Бактерии  '
            ))

            fig.add_trace(go.Scatter3d(
                x=[step_data['best_solution'][0]],
                y=[step_data['best_solution'][1]],
                z=[func(*step_data['best_solution'])],
                mode='markers',
                marker=dict(size=6, color='gold', symbol='diamond'),
                name='Лучшее'
            ))

            result_block = html.Div([
                html.P(f"Итерация: {step_data['iteration'] + 1}/{len(history)}"),
                html.P(f"Лучшая бактерия: x = {step_data['best_solution'][0]:.6f}, y = {step_data['best_solution'][1]:.6f}"),
                html.P(f"f(x, y) = {step_data['best_score']:.6f}")
            ])

            return fig, result_block, no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("bfoa-interval", "interval"),
        Input("bfoa-speed", "value")
    )
    def update_interval(speed):
        return speed

    @app.callback(
        Output("bfoa-pause-button", "children"),
        Input("bfoa-interval", "disabled")
    )
    def update_pause_label(disabled):
        return get_pause_button_text(disabled)
