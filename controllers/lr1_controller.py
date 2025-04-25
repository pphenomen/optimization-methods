from dash.dependencies import Input, Output, State
from dash import html, no_update, callback_context
import dash
import plotly.graph_objs as go
from models.gradient_descent import GradientDescent
from controllers.utils import init_state, reset_state, create_surface_figure, handle_pause, get_pause_button_text
from models.functions import FUNCTIONS

def register_lr1_callbacks(app):
    app.history_store = init_state()

    @app.callback(
        [Output("3d-plot", "figure"),
         Output("execution-results", "children"),
         Output("run-button", "disabled"),
         Output("animation-interval", "disabled"),
         Output("toast", "is_open"),
         Output("toast", "children")],
        [Input("run-button", "n_clicks"),
         Input("animation-interval", "n_intervals"),
         Input("pause-button", "n_clicks"),
         Input("function-selector", "value")],
        [State("x0-input", "value"),
         State("y0-input", "value"),
         State("lr-input", "value"),
         State("maxiter-input", "value"),
         State("3d-plot", "figure"),
         State("animation-interval", "disabled")]
    )
    def update_plot_and_results(run_clicks, n_intervals, pause_clicks, function_key,
                                x0, y0, lr, max_iter, current_figure, interval_disabled):

        ctx = callback_context
        if not ctx.triggered:
            raise dash.exceptions.PreventUpdate

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == "pause-button":
            return handle_pause(app.history_store["history"] is not None, interval_disabled)

        if triggered_id == "function-selector":
            if app.history_store["history"]:
                reset_state(app, "history_store")
                empty_fig = create_surface_figure(function_key)
                return empty_fig, "", False, True, True, "Алгоритм остановлен из-за смены функции"
            if not function_key:
                return no_update, no_update, no_update, no_update, False, ""
            return create_surface_figure(function_key), no_update, no_update, no_update, False, ""

        if triggered_id == "run-button":
            if not function_key:
                return no_update, no_update, no_update, no_update, True, "Пожалуйста, выберите функцию для оптимизации."
            func = FUNCTIONS[function_key]
            gd = GradientDescent(func=func, x0=x0, y0=y0, learning_rate=lr, max_iter=max_iter)
            history, converged, message = gd.run()

            app.history_store.update({
                'history': history,
                'current_step': 0,
                'function_key': function_key,
                'message': message,
                'converged': converged
            })

            fig = create_surface_figure(function_key)
            return fig, html.P("Запуск анимации...", className="text-white"), True, False, False, ""

        if triggered_id == "animation-interval" and app.history_store["history"]:
            history = app.history_store["history"]
            current_step = app.history_store["current_step"]

            if current_step >= len(history):
                final_message = [
                    html.P(app.history_store['message'], className="text-white"),
                    html.Ul([
                        html.Li(f"Итерация {step['iteration']}: x = {step['x']:.4f}, y = {step['y']:.4f}, f(x, y) = {step['f_value']:.4f}")
                        for step in history
                    ])
                ]
                return no_update, final_message, False, True, False, ""

            step = history[current_step]
            app.history_store["current_step"] += 1

            fig = go.Figure(current_figure)
            fig.data = [fig.data[0]]

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

            results = [
                html.P(f"Итерация {step['iteration']}/{len(history)}", className="text-white"),
                html.P(f"x = {step['x']:.4f}, y = {step['y']:.4f}", className="text-white"),
                html.P(f"f(x, y) = {step['f_value']:.4f}", className="text-white"),
                html.P(f"Норма градиента = {step['grad_norm']:.4f}", className="text-white")
            ]
            return fig, results, no_update, no_update, False, ""

        return no_update, no_update, no_update, no_update, False, ""

    @app.callback(
        Output("animation-interval", "interval"),
        Input("animation-speed", "value")
    )
    def update_animation_speed(speed):
        return speed

    @app.callback(
        Output("pause-button", "children"),
        Input("animation-interval", "disabled")
    )
    def update_pause_text(disabled):
        return get_pause_button_text(disabled)
