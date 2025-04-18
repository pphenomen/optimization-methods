import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from views import main_page, lr1_page, lr2_page, lr3_page, lr4_page, lr5_page, lr6_page
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
        "/lr1": lr1_page.layout,
        "/lr2": lr2_page.layout,
        "/lr3": lr3_page.layout,
        "/lr4": lr4_page.layout,
        "/lr5": lr5_page.layout,
        "/lr6": lr6_page.layout
    }.get(pathname, main_page.layout)

register_all_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
