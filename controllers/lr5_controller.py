from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from dash import html, no_update, callback_context
from models.bees import BeesAlgorithm
from models.functions import FUNCTIONS, FUNCTION_NAMES
import numpy as np
import dash

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
                 fig, n_bees, n_iters, n_elite, n_selected_input, n_recruited_elite, n_recruited_selected, radius, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered = ctx.triggered[0]['prop_id'].split('.')[0]
        fig = fig if fig else go.Figure()

        if triggered == "bees-pause-button":
            if not app.bees_state['running']:
                return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
            return no_update, no_update, no_update, not interval_disabled, False, ""

        if triggered == "bees-function-selector" and function_key:
            if app.bees_state["running"]:
                app.bees_state = {
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
                legend=dict(x=0, y=0.95, bgcolor='rgba(255,255,255,0.7)', bordercolor='black', font=dict(size=16), borderwidth=1)
            )
            return fig, no_update, no_update, no_update, False, ""

        if triggered == "bees-run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации"
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

            x = np.linspace(-5, 5, 100)
            y = np.linspace(-5, 5, 100)
            X, Y = np.meshgrid(x, y)
            Z = func(X, Y)
            fig = go.Figure([go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)])
            fig.update_layout(
                title=FUNCTION_NAMES[function_key],
                scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=40),
                legend=dict(x=0, y=0.95, bgcolor='rgba(255,255,255,0.7)', bordercolor='black', font=dict(size=16), borderwidth=1)
            )
            return fig, "Запуск пчелиного алгоритма...", True, False, False, ""

        if triggered == "bees-interval" and app.bees_state['running']:
            step = app.bees_state['current_step']
            history = app.bees_state['history']
            if step >= len(history):
                app.bees_state['running'] = False
                best_bee = history[-1]['best']
                return fig, html.Div([
                    html.P(f"Лучшее решение: x = {best_bee[0]:.4f}, y = {best_bee[1]:.4f}"),
                    html.P(f"Значение функции f(x, y): {best_bee[2]:.4f}")
                ]), False, True, False, ""

            step_data = history[step]
            app.bees_state['current_step'] += 1
            label = f"Итерация {step_data['step']}"

            fig = go.Figure(fig)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['elite']],
                y=[b[1] for b in step_data['elite']],
                z=[b[2] for b in step_data['elite']],
                mode='markers',
                marker=dict(size=5, color='red'),
                name='Элитные',
                text=[label]*len(step_data['elite']),
                hoverinfo='text'
            ))

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['selected']],
                y=[b[1] for b in step_data['selected']],
                z=[b[2] for b in step_data['selected']],
                mode='markers',
                marker=dict(size=4, color='cyan'),
                name='Перспективные         ',
                text=[label]*len(step_data['selected']),
                hoverinfo='text'
            ))

            fig.add_trace(go.Scatter3d(
                x=[b[0] for b in step_data['scouts']],
                y=[b[1] for b in step_data['scouts']],
                z=[b[2] for b in step_data['scouts']],
                mode='markers',
                marker=dict(size=2, color='black'),
                name='Разведчики',
                text=[label]*len(step_data['scouts']),
                hoverinfo='text'
            ))

            best = step_data['best']
            fig.add_trace(go.Scatter3d(
                x=[best[0]], y=[best[1]], z=[best[2]],
                mode='markers',
                marker=dict(size=8, color='gold', symbol='diamond'),
                name='Лучшее',
                text=[f'Лучшее на {label}'],
                hoverinfo='text'
            ))

            return fig, html.Div([
                html.P(f"Итерация: {step_data['step']}/{len(history)}"),
                html.Hr(),
                html.P("Элитные:"),
                *[html.Div(f"  ({b[0]:.2f}, {b[1]:.2f}) -> f = {b[2]:.2f}") for b in step_data['elite']],
                html.P("Перспективные:"),
                *[html.Div(f"  ({b[0]:.2f}, {b[1]:.2f}) -> f = {b[2]:.2f}") for b in step_data['selected']],
                html.P("Разведчики:"),
                *[html.Div(f"  ({b[0]:.2f}, {b[1]:.2f}) -> f = {b[2]:.2f}") for b in step_data['scouts']],
                html.Hr(),
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
        return "Продолжить" if disabled else "Пауза"
    
    @app.callback(
    Output("log-modal", "is_open"),
    Output("bees-modal-results", "children"),
    [Input("open-log-modal", "n_clicks"), Input("close-log-modal", "n_clicks")],
    [State("log-modal", "is_open"), State("bees-results", "children")]
    )
    def toggle_log_modal(open_clicks, close_clicks, is_open, log_data):
        if open_clicks or close_clicks:
            return not is_open, log_data
        return is_open, log_data

    @app.callback(
    Output("bees-results", "children", allow_duplicate=True),
    Input("clear-log", "n_clicks"),
    prevent_initial_call=True
    )
    def clear_logs(_):
        return ""