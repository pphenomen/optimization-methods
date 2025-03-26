from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
from models.gradient_descent import GradientDescent
from models.functions import FUNCTIONS, FUNCTION_NAMES
from dash import html, no_update
import dash

def register_lr1_callbacks(app):
    # Глобальное хранилище для состояния анимации
    app.history_store = {
        'history': None,
        'current_step': 0,
        'function_key': None,
        'message': None,
        'converged': False
    }

    @app.callback(
        [Output("3d-plot", "figure"),
         Output("execution-results", "children"),
         Output("run-button", "disabled"),
         Output("animation-interval", "disabled"),
         Output("animation-controls", "style")],
        [Input("run-button", "n_clicks"),
         Input("animation-interval", "n_intervals"),
         Input("pause-button", "n_clicks")],
        [State("x0-input", "value"),
         State("y0-input", "value"),
         State("lr-input", "value"),
         State("maxiter-input", "value"),
         State("function-selector", "value"),
         State("3d-plot", "figure"),
         State("animation-interval", "disabled")]
    )
    def update_plot_and_results(run_clicks, n_intervals, pause_clicks, 
                               x0, y0, lr, max_iter, function_key, current_figure, interval_disabled):
        ctx = dash.callback_context
        if not ctx.triggered:
            return no_update, no_update, no_update, no_update, no_update

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'run-button' and run_clicks:
            # Инициализация новой оптимизации
            func = FUNCTIONS[function_key]
            gd = GradientDescent(func=func, x0=x0, y0=y0, learning_rate=lr, max_iter=max_iter)
            history, converged, message = gd.run()
            
            # Сохраняем данные для анимации
            app.history_store = {
                'history': history,
                'current_step': 0,
                'function_key': function_key,
                'message': message,
                'converged': converged
            }
            
            # Создаем базовый график
            x_vals = np.linspace(-5, 5, 50)
            y_vals = np.linspace(-5, 5, 50)
            X, Y = np.meshgrid(x_vals, y_vals)
            Z = func(X, Y)
            
            fig = go.Figure(data=[
                go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', opacity=0.8)
            ])
            
            fig.update_layout(
                title=f"{FUNCTION_NAMES[function_key]}",
                scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='f(x, y)'),
                margin=dict(l=0, r=0, b=0, t=30)
            )
            
            return fig, html.P("Запуск анимации...", className="text-white"), True, False, {'display': 'block'}

        elif triggered_id == 'pause-button':
            # Пауза/продолжение анимации
            return no_update, no_update, no_update, not interval_disabled, no_update

        elif triggered_id == 'animation-interval' and app.history_store['history']:
            # Обработка шага анимации
            history = app.history_store['history']
            current_step = app.history_store['current_step']
            
            if current_step >= len(history):
                # Анимация завершена
                final_message = [
                    html.P(app.history_store['message'], className="text-white"),
                    html.Ul([
                        html.Li(f"Итерация {step['iteration']}: x = {step['x']:.4f}, y = {step['y']:.4f}, f(x, y) = {step['f_value']:.4f}")
                        for step in history
                    ])
                ]
                return no_update, final_message, False, True, no_update
            
            # Получаем данные для текущего шага
            step = history[current_step]
            app.history_store['current_step'] += 1
            
            # Обновляем график
            fig = go.Figure(current_figure)
            
            # Очищаем предыдущую траекторию (оставляем только surface)
            fig.data = [fig.data[0]]
            
            # Добавляем траекторию до текущей точки
            trajectory_x = [h["x"] for h in history[:current_step+1]]
            trajectory_y = [h["y"] for h in history[:current_step+1]]
            trajectory_z = [h["f_value"] for h in history[:current_step+1]]
            
            fig.add_trace(go.Scatter3d(
                x=trajectory_x,
                y=trajectory_y,
                z=trajectory_z,
                mode='lines+markers',
                marker=dict(size=5, color='red'),
                line=dict(color='red', width=2),
                name='Траектория'
            ))
            
            # Обновляем результаты выполнения
            results = [
                html.P(f"Итерация {step['iteration']}/{len(history)}", className="text-white"),
                html.P(f"Текущая точка: x = {step['x']:.4f}, y = {step['y']:.4f}", className="text-white"),
                html.P(f"Значение функции: {step['f_value']:.4f}", className="text-white"),
                html.P(f"Норма градиента: {step['grad_norm']:.4f}", className="text-white")
            ]
            
            return fig, results, no_update, no_update, no_update

        return no_update, no_update, no_update, no_update, no_update

    # Добавляем callback для управления скоростью анимации
    @app.callback(
        Output("animation-interval", "interval"),
        Input("animation-speed", "value")
    )
    def update_animation_speed(speed):
        return speed