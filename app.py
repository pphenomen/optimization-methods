import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from views import main_page, lr1_page, lr2_page, lr3_page
from controllers import register_all_callbacks

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY], suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content', children=main_page.layout)
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    return {
        "/lr1": lr1_page.layout
    }.get(pathname, main_page.layout)

register_all_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
