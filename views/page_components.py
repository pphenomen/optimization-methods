from dash import dcc, html
import dash_bootstrap_components as dbc
from models.functions import FUNCTION_NAMES

def create_navbar(title: str, color: str = "secondary"):
    return dbc.NavbarSimple(
        children=[
            dbc.Button("Назад", href="/", color="secondary",
                       className="position-absolute",
                       style={"top": "15px", "right": "15px", "zIndex": "1000"})
        ],
        brand=title,
        color=color,
        dark=True,
        brand_style={"fontSize": "26px", "fontWeight": "bold"},
        className="bg-dark",
    )

def create_graph(graph_id: str):
    return dcc.Graph(
        id=graph_id,
        config={"scrollZoom": True},
        style={"height": "98%", "width": "130%"}
    )

def create_function_dropdown(dropdown_id: str, default: str = None):
    return dbc.InputGroup([
        dbc.InputGroupText("Функция"),
        dcc.Dropdown(
            id=dropdown_id,
            options=[{"label": FUNCTION_NAMES[k], "value": k} for k in FUNCTION_NAMES],
            placeholder="Выберите функцию",
            clearable=False,
            value=default,
            style={"flex": "1"}
        )
    ], className='mb-2 text-dark')

def create_toast(toast_id: str, message="Сначала запустите алгоритм"):
    return dbc.Toast(
        message,
        id=toast_id,
        header="Предупреждение",
        is_open=False,
        dismissable=True,
        icon="danger",
        duration=5000,
        style={
            "position": "fixed", "top": "50%", "left": "50%",
            "transform": "translate(-50%, -50%)", "zIndex": 9999,
            "width": "15%", "height": "15%", "text-align": "center"
        }
    )


def create_animation_controls(pause_btn_id: str, slider_id: str):
    return html.Div([
        dbc.Button(id=pause_btn_id, children="Пауза", color="primary", className="mt-2 w-100"),
        dcc.Slider(
            id=slider_id,
            min=150, max=2000, step=100, value=1000,
            marks={150: "Быстро", 1000: "Средне", 2000: "Медленно"},
            className="mt-2"
        )
    ])


def create_results_block(results_id: str):
    return html.Div([
        html.H4("Выполнение и результаты", className="mt-2 text-white"),
        html.Div(
            id=results_id,
            className="p-3 rounded mb-3 bg-secondary text-white",
            style={"height": "150px", "overflowY": "scroll"}
        )
    ])


def create_log_modal(prefix: str):
    return html.Div([
        html.Div([
            dbc.Button("Открыть логи", id=f"{prefix}-open-log-modal", color="primary", size="sm", className="me-2 flex-fill"),
            dbc.Button("Очистить логи", id=f"{prefix}-clear-log", color="danger", size="sm", className="flex-fill"),
        ], className="d-flex mt-2"),

        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Подробные логи")),
            dbc.ModalBody(html.Div(
                id=f"{prefix}-modal-results",
                className="p-3 rounded mb-3 bg-secondary text-white",
                style={"maxHeight": "70vh", "overflowY": "auto"}
            )),
            dbc.ModalFooter(dbc.Button("Закрыть", id=f"{prefix}-close-log-modal", className="ms-auto", n_clicks=0))
        ], backdrop=False, id=f"{prefix}-log-modal", is_open=False, size="xl", scrollable=True)
    ])

