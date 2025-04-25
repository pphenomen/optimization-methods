import numpy as np
import plotly.graph_objs as go
from dash import no_update
from models.functions import FUNCTIONS, FUNCTION_NAMES

def init_state():
    return {
        'history': None,
        'current_step': 0,
        'function_key': None,
        'message': None,
        'converged': False
    }

def reset_state(app, state_attr):
    setattr(app, state_attr, init_state())

def create_surface_figure(function_key):
    func = FUNCTIONS[function_key]
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)

    fig = go.Figure([
        go.Surface(z=Z, x=X, y=Y, colorscale="Viridis", opacity=0.8)
    ])
    fig.update_layout(
        title=FUNCTION_NAMES[function_key],
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='f(x, y)'),
        margin=dict(l=0, r=0, b=0, t=40),
        legend=dict(x=0, y=0.95, bgcolor='rgba(255,255,255,0.7)', font=dict(size=16), bordercolor='black', borderwidth=1)
    )
    return fig

def handle_pause(is_running, interval_disabled):
    if not is_running:
        return no_update, no_update, no_update, no_update, True, "Сначала запустите алгоритм"
    return no_update, no_update, no_update, not interval_disabled, False, ""

def get_pause_button_text(disabled):
    return "Продолжить" if disabled else "Пауза"
