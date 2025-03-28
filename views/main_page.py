from dash import dcc, html
import dash_bootstrap_components as dbc

layout = dbc.Container([
    html.H1("Методы поисковой оптимизации", className="text-center mt-4 text-white"),
    html.Hr(),
    dbc.Row([
        dbc.Col(dbc.Button("Лабораторная работа 1", href="/lr1", color="secondary", className="btn-lg d-grid gap-2"), width=6),
    ], className="mt-4 justify-content-center"),
    dbc.Row([
        dbc.Col(dbc.Button("Лабораторная работа 2", href="/lr2", color="secondary", className="btn-lg d-grid gap-2"), width=6),
    ], className="mt-4 justify-content-center"),
    dbc.Row([
        dbc.Col(dbc.Button("Лабораторная работа 3", href="/lr3", color="secondary", className="btn-lg d-grid gap-2"), width=6),
    ], className="mt-4 justify-content-center"),
    dbc.Row([
        dbc.Col(dbc.Button("Лабораторная работа 4", href="/lr4", color="secondary", className="btn-lg d-grid gap-2"), width=6),
    ], className="mt-4 justify-content-center"),
], className="p-5 bg-dark")