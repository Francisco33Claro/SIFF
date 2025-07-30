import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import os

# App principal
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Menu lateral
menus = [
    ("menu", "Início", "icon_menu.svg"),
    ("lancamentos", "Lançamento Unificado", "icon_lancamentos.svg"),
    ("receitas", "Receitas", "icon_receitas.svg"),
    ("despesas", "Despesas", "icon_despesas.svg"),
    ("relatorios", "Relatórios", "icon_relatorios.svg"),
    ("dashboards", "Dashboard", "icon_dashboards.svg"),
    ("configuracoes", "Configurações", "icon_configuracoes.svg"),
]

# Sidebar com botão de logout ao final
sidebar = html.Div([
    html.H2("SIFF", className="display-6", style={"textAlign": "center", "marginTop": "10px"}),
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink(
                [
                    html.Img(src=f"/assets/{icone}", height="40px", style={"marginRight": "10px"}),
                    html.Span(label, className="ms-2")
                ],
                href=f"/menu/{rota}",
                active="exact",
                style={"display": "flex", "alignItems": "center", "padding": "10px"}
            )
            for rota, label, icone in menus
        ] + [
            html.Hr(),
            dbc.NavLink(
                [
                    html.Img(src="/assets/icon_sair.svg", height="40px", style={"marginRight": "10px"}),
                    html.Span("Sair", className="ms-2")
                ],
                href="/",
                style={"display": "flex", "alignItems": "center", "padding": "10px", "color": "red"}
            )
        ],
        vertical=True,
        pills=True,
    ),
    html.Div([
        html.Hr(),
        html.H5("Sobre o Sistema", style={"textAlign": "center", "marginTop": "20px"}),
        html.P("SIFF - Sistema de Finanças Familiar", style={"fontSize": "12px", "textAlign": "center"}),
        html.P("Versão 1.0", style={"fontSize": "12px", "textAlign": "center"}),
        html.P("Desenvolvido por Francisco Claro", style={"fontSize": "10px", "textAlign": "center", "color": "gray"})
    ], style={"marginTop": "auto", "padding": "10px"})
], style={
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "250px",
    "padding": "20px",
    "backgroundColor": "#f8f9fa",
    "overflowY": "auto"
})

# Conteúdo principal
content = html.Div(id="page-content", style={"marginLeft": "270px", "padding": "20px"})

# Layout com menu lateral + conteúdo
menu_layout = html.Div([
    sidebar,
    content
])

# Layout de login
login_layout = html.Div([
    html.Div([
        html.H2("Login do SIFF - Sistema de Finanças Familiar", style={
            "textAlign": "center", "color": "white", "marginTop": "30px"
        }),
        html.Div("Usuário:", style={"color": "white"}),
        dcc.Input(id="input-usuario", type="text", placeholder="Digite seu usuário", style={"width": "100%"}),
        html.Br(), html.Br(),
        html.Div("Senha:", style={"color": "white"}),
        dcc.Input(id="input-senha", type="password", placeholder="Digite sua senha", style={"width": "100%"}),
        html.Br(), html.Br(),
        html.Button("Entrar", id="botao-login", n_clicks=0, style={"width": "100%"}),
        html.Div(id="mensagem-login", style={"color": "yellow", "marginTop": "10px"})
    ], style={
        "width": "30%", "margin": "auto", "padding": "30px",
        "backgroundColor": "rgba(0, 0, 0, 0.6)", "borderRadius": "10px"
    })
], style={
    "backgroundImage": "url('/assets/bg_login.jpg')",
    "backgroundSize": "cover", "height": "100vh", "display": "flex", "alignItems": "center"
})

# Layout geral
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="pagina-conteudo")
])

# Callback para login
@app.callback(
    Output("mensagem-login", "children"),
    Output("url", "pathname"),
    Input("botao-login", "n_clicks"),
    State("input-usuario", "value"),
    State("input-senha", "value"),
)
def login(n_clicks, usuario, senha):
    if n_clicks > 0:
        if usuario == "admin" and senha == "admin123":
            return "", "/menu/dashboards"
        return "Usuário ou senha incorretos.", dash.no_update
    return "", dash.no_update

# Callback para trocar o layout principal
@app.callback(
    Output("pagina-conteudo", "children"),
    Input("url", "pathname")
)
def trocar_layout(pathname):
    if pathname and pathname.startswith("/menu"):
        return menu_layout
    return login_layout

# Callback para renderizar o conteúdo do menu
@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def renderizar_pagina_menu(pathname):
    if pathname in ["/menu", "/menu/menu", "/menu/dashboards"]:
        return html.H1("Página de Dashboard", style={"textAlign": "center", "marginTop": "50px"})
    elif pathname == "/menu/lancamentos":
        return html.H1("Página de Lançamento Unificado", style={"textAlign": "center", "marginTop": "50px"})
    elif pathname == "/menu/receitas":
        return html.H1("Página de Receitas", style={"textAlign": "center", "marginTop": "50px"})
    elif pathname == "/menu/despesas":
        return html.H1("Página de Despesas", style={"textAlign": "center", "marginTop": "50px"})
    elif pathname == "/menu/relatorios":
        return html.H1("Página de Relatórios", style={"textAlign": "center", "marginTop": "50px"})
    elif pathname == "/menu/configuracoes":
        return html.H1("Página de Configurações", style={"textAlign": "center", "marginTop": "50px"})
    return html.H1(f"Página não encontrada: {pathname}", style={"textAlign": "center", "marginTop": "50px"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
