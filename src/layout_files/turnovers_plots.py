import dash_bootstrap_components as dbc

from dash import dcc, html


TURNOVERS_LAYOUT = [
    html.H2('Average Weekly Turnovers per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-TO",
                        children=[dcc.Graph(id="avg_TO")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Turnovers Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-TO",
                        children=[dcc.Graph(id="graph_TO")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Turnovers Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-TO-weekly",
                        children=[dcc.Graph(id="graph_TO_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
