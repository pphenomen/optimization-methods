from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from models.genetic_algorithm import GeneticAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
from dash import html, no_update, callback_context
import dash

def register_lr3_callbacks(app):
    app.ga_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'function_key': None
    }

    @app.callback(
        [Output("rosenbrock-plot", "figure"),
         Output("ga-results", "children"),
         Output("ga-run-button", "disabled"),
         Output("ga-interval", "disabled"),
         Output("ga-toast", "is_open"),
         Output("ga-toast", "children")],
        [Input("ga-run-button", "n_clicks"),
         Input("ga-interval", "n_intervals"),
         Input("ga-pause-button", "n_clicks"),
         Input("function-selector", "value")],
        [State("rosenbrock-plot", "figure"),
         State("ga-pop-size", "value"),
         State("ga-mutation-rate", "value"),
         State("ga-generations", "value"),
         State("ga-interval", "disabled")]
    )
    def run_ga(n_clicks, n_intervals, pause_clicks, function_key, current_figure, pop_size, mutation_rate, generations, interval_disabled):
        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'ga-pause-button':
            if not app.ga_state['running']:
                return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
            new_state = not interval_disabled
            return no_update, no_update, no_update, new_state, False, ""

        if triggered_id == "ga-run-button" and not function_key:
            return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации."
        
        func = FUNCTIONS[function_key]

        if triggered_id == 'ga-run-button' and n_clicks:
            ga = GeneticAlgorithm(func=func, pop_size=pop_size,
                                  mutation_rate=mutation_rate,
                                  generations=generations)
            best, history = ga.run()

            app.ga_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'function_key': function_key
            })

            x = np.linspace(-2, 2, 100)
            y = np.linspace(-1, 3, 100)
            X, Y = np.meshgrid(x, y)
            Z = func(X, Y)

            fig = go.Figure([
                go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)
            ])
            fig.update_layout(
                title=FUNCTION_NAMES[function_key],
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=40)
            )

            return fig, "Запуск алгоритма...", True, False, False, ""

        elif triggered_id == 'ga-interval' and app.ga_state['running']:
            hist = app.ga_state['history']
            step = app.ga_state['current_step']
            func = FUNCTIONS[app.ga_state['function_key']]

            if step >= len(hist):
                app.ga_state['running'] = False
                best = hist[-1]
                return current_figure, html.Div([
                    html.P(f"Лучшее решение: x = {best[0]:.4f}, y = {best[1]:.4f}"),
                    html.P(f"Значение функции f(x): {best[2]:.4f}")
                ]), False, True, False, ""

            point = hist[step]
            app.ga_state['current_step'] += 1

            fig = go.Figure(current_figure)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            xs = [h[0] for h in hist[:step+1]]
            ys = [h[1] for h in hist[:step+1]]
            zs = [h[2] for h in hist[:step+1]]

            fig.add_trace(go.Scatter3d(
                x=xs, y=ys, z=zs,
                mode='lines+markers',
                marker=dict(color='red', size=4),
                line=dict(color='red', width=2),
                name='Эволюция'
            ))

            result_text = html.Div([
                html.P(f"Поколение: {step + 1}/{len(hist)}"),
                html.P(f"x = {point[0]:.4f}, y = {point[1]:.4f}, f(x, y) = {point[2]:.4f}")
            ])

            return fig, result_text, no_update, no_update, False, ""

        elif triggered_id == 'function-selector':
            func = FUNCTIONS[function_key]
            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = func(X, Y)

            fig = go.Figure([
                go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)])
            fig.update_layout(
                title=FUNCTION_NAMES[function_key],
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=40)
            )
            
            return fig, "", False, True, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("ga-interval", "interval"),
        Input("ga-animation-speed", "value")
    )
    def update_speed(speed):
        return speed

    @app.callback(
        Output("ga-pause-button", "children"),
        Input("ga-interval", "disabled")
    )
    def update_pause_button_text(disabled):
        return "Продолжить" if disabled else "Пауза"