from dash import callback_context, html, no_update
from dash.dependencies import Input, Output, State
from models.immune_algorithm import ImmuneAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
import plotly.graph_objs as go
import numpy as np
import dash

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
            if not app.ais_state['running']:
                return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
            return no_update, no_update, no_update, not interval_disabled, False, ""

        if triggered == "ais-function-selector" and function_key:
            if app.ais_state["running"]:
                app.ais_state = {
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
            return fig, "Запуск иммунного алгоритма...", True, False, False, ""

        if triggered == "ais-interval" and app.ais_state['running']:
            step = app.ais_state['current_step']
            history = app.ais_state['history']
            if step >= len(history):
                app.ais_state['running'] = False
                best_antibody = history[-1]['best']
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best_antibody[0]:.4f}, y = {best_antibody[1]:.4f}"),
                    html.P(f"Значение функции f(x, y): {history[-1]['score']:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            app.ais_state['current_step'] += 1
            label = f"Итерация {step_data['iteration']}"

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[a[0] for a in step_data['population']],
                y=[a[1] for a in step_data['population']],
                z=[FUNCTIONS[app.ais_state['function_key']](a[0], a[1]) for a in step_data['population']],
                mode='markers',
                marker=dict(size=4, color='cyan'),
                name='Антитела      ',
                text=[label]*len(step_data['population']),
                hoverinfo='text'
            ))

            fig.add_trace(go.Scatter3d(
                x=[step_data['best'][0]],
                y=[step_data['best'][1]],
                z=[step_data['score']],
                mode='markers',
                marker=dict(size=6, color='gold', symbol='diamond'),
                name='Лучшее',
                text=[f'Лучшее на {label}'],
                hoverinfo='text'
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
        return "Продолжить" if disabled else "Пауза"