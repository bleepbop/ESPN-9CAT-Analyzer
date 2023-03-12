import dash_bootstrap_components as dbc

from dash import dcc, html


STEALS_LAYOUT = [
    html.H2('Weekly Steal Averages per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-STL",
                        children=[dcc.Graph(id="avg_STL")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Steals Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-STL",
                        children=[dcc.Graph(id="graph_STL")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Steals Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-STL-weekly",
                        children=[dcc.Graph(id="graph_STL_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]