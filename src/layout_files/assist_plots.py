import dash_bootstrap_components as dbc

from dash import dcc, html


ASSISTS_LAYOUT = [
    html.H2('Weekly Assist Averages per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-AST",
                        children=[dcc.Graph(id="avg_AST")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Assists Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-AST",
                        children=[dcc.Graph(id="graph_AST")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Assists Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-AST-weekly",
                        children=[dcc.Graph(id="graph_AST_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
