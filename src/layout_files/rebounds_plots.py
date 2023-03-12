import dash_bootstrap_components as dbc

from dash import dcc, html

REBOUNDS_LAYOUT = [
    html.H2('Average Weekly Rebounds per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-REB",
                        children=[dcc.Graph(id="avg_REB")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Rebounds Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-REB",
                        children=[dcc.Graph(id="graph_REB")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Rebounds Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-REB-weekly",
                        children=[dcc.Graph(id="graph_REB_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]