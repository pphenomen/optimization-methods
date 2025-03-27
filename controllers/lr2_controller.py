from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from scipy.optimize import minimize
from dash import html, no_update
import dash

def register_lr2_callbacks(app):
    app.optimization_state = {
        'history': [],
        'current_step': 0,
        'running': False,
        'interval_disabled': True,
        'result': None,
        'objective': None
    }

    @app.callback(
        [Output("qp-graph", "figure"),
         Output("qp-results", "children"),
         Output("qp-run-button", "disabled"),
         Output("interval-component", "disabled"),
         Output("qp-animation-controls", "style")],
        [Input("qp-run-button", "n_clicks"),
         Input("interval-component", "n_intervals"),
         Input("qp-pause-button", "n_clicks")],
        [State("qp-graph", "figure"),
         State("interval-component", "disabled")]
    )
    def run_qp(n_clicks, n_intervals, pause_clicks, current_figure, interval_disabled):
        ctx = dash.callback_context

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Задача: f(x) = 2x1² + 3x2² + 4x1x2 - 6x1 - 3x2 → min
        Q = [[4, 4], [4, 6]]  # 2Q
        c = [-6, -3]
        A = [[1, 1], [2, 3]]
        b = [1, 4]
        bounds = [(0, None), (0, None)]

        def objective(x):
            return 0.5 * np.dot(x, np.dot(Q, x)) + np.dot(c, x)

        constraints = [
            {'type': 'ineq', 'fun': lambda x, A=A[i], b=b[i]: b - np.dot(A, x)}
            for i in range(len(b))
        ]

        if triggered_id == 'qp-run-button' and n_clicks:
            history = []
            def callback(xk):
                history.append({
                    'x': xk.copy(),
                    'f': objective(xk),
                    'constraints': [float(np.ravel(con['fun'](xk))[0]) for con in constraints]
                })

            result = minimize(
                objective,
                x0=[0.5, 0.5],
                method='SLSQP',
                bounds=bounds,
                constraints=constraints,
                callback=callback
            )

            if not result.success:
                return go.Figure(), html.P(f"Ошибка: {result.message}", className="text-danger"), False, True, {'display': 'none'}

            app.optimization_state.update({
                'history': history,
                'current_step': 0,
                'running': True,
                'interval_disabled': False,
                'result': result,
                'objective': objective
            })

            # Поверхность
            X, Y = np.meshgrid(np.linspace(-1, 3, 60), np.linspace(-1, 3, 60))
            Z = np.array([[objective([x, y]) for x, y in zip(row_x, row_y)] for row_x, row_y in zip(X, Y)])

            fig = go.Figure([
                go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)
            ])
            fig.update_layout(
                scene=dict(
                    xaxis_title='x1',
                    yaxis_title='x2',
                    zaxis_title='f(x1,x2)'
                ),
                margin=dict(l=0, r=0, b=0, t=40)
            )

            return fig, "Запуск оптимизации...", True, False, {'display': 'block'}

        elif triggered_id == "qp-pause-button":
            # Пауза / Продолжить
            new_state = not interval_disabled
            app.optimization_state['interval_disabled'] = new_state
            return no_update, no_update, no_update, new_state, no_update

        elif triggered_id == 'interval-component' and app.optimization_state['running']:
            history = app.optimization_state['history']
            current_step = app.optimization_state['current_step']
            result = app.optimization_state['result']

            if current_step >= len(history):
                app.optimization_state['running'] = False
                return current_figure, html.Div([
                    html.P(f"Оптимальное решение: x1 = {result.x[0]:.4f}, x2 = {result.x[1]:.4f}"),
                    html.P(f"Значение функции: {result.fun:.4f}"),
                    html.P(f"Итераций: {result.nit}")
                ]), False, True, no_update

            point = history[current_step]
            app.optimization_state['current_step'] += 1

            fig = go.Figure(current_figure)
            fig.data = [trace for trace in fig.data if isinstance(trace, go.Surface)]

            trajectory_x = [h['x'][0] for h in history[:current_step+1]]
            trajectory_y = [h['x'][1] for h in history[:current_step+1]]
            trajectory_z = [h['f'] for h in history[:current_step+1]]

            fig.add_trace(go.Scatter3d(
                x=trajectory_x,
                y=trajectory_y,
                z=trajectory_z,
                mode='lines+markers',
                marker=dict(size=5, color='red'),
                line=dict(color='red', width=2),
                name='Траектория'
            ))

            result_text = html.Div([
                html.P(f"Итерация: {current_step}/{len(history)}"),
                html.P(f"Текущая точка: x1 = {point['x'][0]:.4f}, x2 = {point['x'][1]:.4f}"),
                html.P(f"Значение функции: {point['f']:.4f}"),
                html.P(f"Ограничения: {[f'{c:.2f}' for c in point['constraints']]}"),
            ])

            return fig, result_text, no_update, no_update, no_update

        return no_update, no_update, no_update, no_update, no_update

    # Слайдер скорости
    @app.callback(
        Output("interval-component", "interval"),
        Input("qp-animation-speed", "value")
    )
    def update_qp_animation_speed(speed):
        return speed
