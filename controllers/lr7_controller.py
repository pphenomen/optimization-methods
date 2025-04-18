from dash import callback_context, html, no_update
from dash.dependencies import Input, Output, State
from models.functions import FUNCTIONS, FUNCTION_NAMES
import plotly.graph_objs as go
import numpy as np
import dash

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
            if not app.bfoa_state['running']:
                return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
            return no_update, no_update, no_update, not interval_disabled, False, ""

        if triggered == "bfoa-function-selector" and function_key:
            if app.bfoa_state["running"]:
                app.bfoa_state = {
                    'history': [],
                    'current_step': 0,
                    'running': False,
                    'function_key': None
                }
                empty_fig = go.Figure()
                empty_fig.update_layout(
                    scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                    margin=dict(l=0, r=0, b=0, t=30)
                )
                return empty_fig, "", False, True, True, "Работа алгоритма остановлена из-за смены функции"
            
            func = FUNCTIONS[function_key]
            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = func(X, Y)
            fig = go.Figure([go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)])
            fig.update_layout(
                title=FUNCTION_NAMES[function_key],
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=40),
                legend=dict(x=0, y=0.95, bgcolor='rgba(255,255,255,0.7)', font=dict(size=16), bordercolor='black', borderwidth=1)
            )
            return fig, no_update, no_update, no_update, False, ""

        if triggered == "bfoa-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию"
            
            history = []
            for i in range(n_iters):
                history.append({
                    'iteration': i,
                    'population': [np.random.uniform(-5, 5, 2) for _ in range(n_bacteria)],
                    'best': np.random.uniform(-5, 5, 2),
                    'score': np.random.uniform(0, 10)
                })
            
            app.bfoa_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            func = FUNCTIONS[function_key]
            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = func(X, Y)
            fig = go.Figure([go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)])
            fig.update_layout(
                title=FUNCTION_NAMES[function_key],
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=40),
                legend=dict(x=0, y=0.95, bgcolor='rgba(255,255,255,0.7)', font=dict(size=16), bordercolor='black', borderwidth=1)
            )
            return fig, "Запуск бактериального алгоритма...", True, False, False, ""

        if triggered == "bfoa-interval" and app.bfoa_state['running']:
            step = app.bfoa_state['current_step']
            history = app.bfoa_state['history']
            if step >= len(history):
                app.bfoa_state['running'] = False
                best_bacteria = history[-1]['best']
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best_bacteria[0]:.4f}, y = {best_bacteria[1]:.4f}"),
                    html.P(f"Значение функции f(x, y): {history[-1]['score']:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            app.bfoa_state['current_step'] += 1
            label = f"Итерация {step_data['iteration']}"

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[a[0] for a in step_data['population']],
                y=[a[1] for a in step_data['population']],
                z=[FUNCTIONS[app.bfoa_state['function_key']](a[0], a[1]) for a in step_data['population']],
                mode='markers',
                marker=dict(size=4, color='cyan'),
                name='Бактерии      ',
                text=[label]*len(step_data['population']),
                hoverinfo='text'
            ))

            fig.add_trace(go.Scatter3d(
                x=[step_data['best'][0]],
                y=[step_data['best'][1]],
                z=[step_data['score']],
                mode='markers',
                marker=dict(size=6, color='gold', symbol='diamond'),
                name='Лучшая',
                text=[f'Лучшая на {label}'],
                hoverinfo='text'
            ))

            result_block = html.Div([
                html.P(f"Итерация: {step_data['iteration'] + 1}/{len(history)}"),
                html.P(f"Лучшая бактерия: x = {step_data['best'][0]:.4f}, y = {step_data['best'][1]:.4f}"),
                html.P(f"f(x, y) = {step_data['score']:.4f}")
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
        return "Продолжить" if disabled else "Пауза"