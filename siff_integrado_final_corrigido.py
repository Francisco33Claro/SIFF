import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import os
from datetime import datetime

app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

CAMINHO_ARQUIVO = "dados/lancamentos_unificados.csv"

categorias_por_tipo = {
    "Receita": ["Salário", "Renda Extra", "Outros"],
    "Despesa": ["Moradia", "Transporte", "Alimentação", "Saúde", "Educação", "Lazer"]
}

menus = [
    ("menu", "Início", "icon_menu.svg"),
    ("lancamentos", "Lançamento Unificado", "icon_lancamentos.svg"),
    ("receitas", "Receitas", "icon_receitas.svg"),
    ("despesas", "Despesas", "icon_despesas.svg"),
    ("relatorios", "Relatórios", "icon_relatorios.svg"),
    ("dashboards", "Dashboard", "icon_dashboards.svg"),
    ("configuracoes", "Configurações", "icon_configuracoes.svg"),
]

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

content = html.Div(id="page-content", style={"marginLeft": "270px", "padding": "20px"})

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

menu_layout = html.Div([
    sidebar,
    dbc.Toast("Lançamento adicionado com sucesso!", id="mensagem-sucesso", header="Sucesso", icon="success",
              duration=3000, is_open=False, style={"position": "fixed", "top": 20, "right": 20, "zIndex": 9999}),
    content
])

def layout_lancamentos_unificados(usuario_logado):
    return html.Div([
        html.H2("➕ Lançamento Unificado de Receitas e Despesas", className="text-center my-4"),

        dbc.Row([
            dbc.Col([
                dbc.Label("📅 Data"),
                dcc.DatePickerSingle(id='data', placeholder='Selecione a data',
                                     display_format='DD/MM/YYYY',
                                     style={"width": "100%"})
            ], md=2),
            dbc.Col([
                dbc.Label("💼 Tipo"),
                dcc.Dropdown(id='tipo',
                             options=[{'label': t, 'value': t} for t in categorias_por_tipo.keys()],
                             placeholder='Selecione o tipo')
            ], md=2),
            dbc.Col([
                dbc.Label("📁 Categoria"),
                dcc.Dropdown(id='categoria', placeholder="Selecione a categoria")
            ], md=2),
            dbc.Col([
                dbc.Label("📝 Descrição"),
                dbc.Input(id='descricao', placeholder='Ex: Supermercado', type='text')
            ], md=3),
            dbc.Col([
                dbc.Label("💰 Valor (R$)"),
                dbc.Input(id='valor', placeholder='0.00', type='number', min=0)
            ], md=3),
        ], className="mb-3"),

        dbc.Button("Adicionar Lançamento", id='adicionar', color='primary', className="mb-4"),
        html.Div(id='tabelas-lancamentos')
    ])

@app.callback(
    Output("mensagem-login", "children"),
    Output("url", "pathname"),
    State("input-usuario", "value"),
    State("input-senha", "value"),
    Input("botao-login", "n_clicks"),
)
def login(usuario, senha, n_clicks):
    if n_clicks > 0:
        if usuario == "admin" and senha == "admin123":
            return "", "/menu/dashboards"
        return "Usuário ou senha incorretos.", dash.no_update
    return "", dash.no_update

@app.callback(Output("pagina-conteudo", "children"), Input("url", "pathname"))
def trocar_layout(pathname):
    if pathname and pathname.startswith("/menu"):
        return menu_layout
    return login_layout

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def renderizar_conteudo(pathname):
    if pathname == "/menu/lancamentos":
        return layout_lancamentos_unificados("admin")
    return html.H1("Página em construção", style={"textAlign": "center", "marginTop": "50px"})

@app.callback(Output('categoria', 'options'), Input('tipo', 'value'))
def atualizar_categorias(tipo):
    if tipo:
        return [{'label': c, 'value': c} for c in categorias_por_tipo[tipo]]
    return []

@app.callback(
    Output('tabelas-lancamentos', 'children'),
    Output('mensagem-sucesso', 'is_open'),
    Input('adicionar', 'n_clicks'),
    State('data', 'date'),
    State('tipo', 'value'),
    State('categoria', 'value'),
    State('descricao', 'value'),
    State('valor', 'value')
)
def adicionar_lancamento(n_clicks, data, tipo, categoria, descricao, valor):
    if not n_clicks or not all([data, tipo, categoria, descricao, valor]):
        return gerar_tabelas(), False

    usuario = "admin"
    df = pd.read_csv(CAMINHO_ARQUIVO) if os.path.exists(CAMINHO_ARQUIVO) else pd.DataFrame(
        columns=['Data', 'Tipo', 'Categoria', 'Descrição', 'Valor', 'Usuário'])

    nova_linha = pd.DataFrame([{
        'Data': datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y"),
        'Tipo': tipo,
        'Categoria': categoria,
        'Descrição': descricao,
        'Valor': float(valor),
        'Usuário': usuario
    }])

    df = pd.concat([df, nova_linha], ignore_index=True)
    df.to_csv(CAMINHO_ARQUIVO, index=False)

    return gerar_tabelas(), True

def gerar_tabelas():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []

    df = pd.read_csv(CAMINHO_ARQUIVO)
    df_credito = df[df["Tipo"] == "Receita"]
    df_debito = df[df["Tipo"] == "Despesa"]
    subtotal = df_credito["Valor"].sum() - df_debito["Valor"].sum()

    def tabela_formatada(dataframe):
        return dbc.Table.from_dataframe(
            dataframe, striped=True, bordered=True, hover=True, className="mt-2")

    return html.Div([
        html.H5("💵 Lançamentos - Crédito (Receitas)", className="text-success mt-4"),
        tabela_formatada(df_credito),
        html.H5("💳 Lançamentos - Débito (Despesas)", className="text-danger mt-4"),
        tabela_formatada(df_debito),
        html.H5("📊 Subtotal (Receitas - Despesas):", className="mt-4"),
        html.H3(f"R$ {subtotal:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), className="text-success")
    ])

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Div(id="pagina-conteudo")
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)