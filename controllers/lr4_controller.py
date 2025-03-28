from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash import html, no_update, callback_context
from models.pso import ParticleSwarmOptimizer
from models.functions import FUNCTIONS, FUNCTION_NAMES
import numpy as np
import dash

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
     Input("function-selector", "value")],
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

        triggered = ctx.triggered[0]['prop_id'].split('.')[0]
        fig = fig if fig else go.Figure()
        
        if triggered == "pso-run-button" and not function_key:
            return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации."
    
        func = FUNCTIONS[function_key]

        if triggered == "function-selector":
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

            return fig, no_update, no_update, no_update, False, ""

        if triggered == "pso-pause-button":
            if not app.pso_state['running']:
                return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
            return no_update, no_update, no_update, not interval_disabled, False, ""

        if triggered == "pso-run-button" and n_clicks and n_clicks > 0:
            optimizer = ParticleSwarmOptimizer(
                func=func,
                num_particles=n_particles,
                iterations=n_iters,
                inertia=inertia,
                cognitive=cognitive,
                social=social
            )
            best_pos, best_val, history = optimizer.optimize()

            app.pso_state.update({
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
                margin=dict(l=0, r=0, b=0, t=40)
            )

            return fig, "Запуск оптимизации...", True, False, False, ""

        elif triggered == "pso-interval" and app.pso_state['running']:
            step = app.pso_state['current_step']
            history = app.pso_state['history']

            if step >= len(history):
                app.pso_state['running'] = False
                pos, val = history[-1]
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {pos[0]:.4f}, y = {pos[1]:.4f}"),
                    html.P(f"Значение функции f(x): {val:.4f}")
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
                marker=dict(color='red', size=4),
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
    def update_pause_label(disabled):
        return "Продолжить" if disabled else "Пауза"
