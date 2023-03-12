import dash_bootstrap_components as dbc

from dash import dcc, html


BLOCKS_LAYOUT = [
    html.H2('Weekly Block Averages per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-BLK",
                        children=[dcc.Graph(id="avg_BLK")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Blocks Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-BLK",
                        children=[dcc.Graph(id="graph_BLK")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Blocks Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-BLK-weekly",
                        children=[dcc.Graph(id="graph_BLK_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
