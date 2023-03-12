import dash_bootstrap_components as dbc

from dash import dcc, html


THREE_POINT_FIELD_GOALS_LAYOUT = [
    html.H2('Average Weekly Made 3 Pointers per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-3PTM",
                        children=[dcc.Graph(id="avg_3PTM")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Made 3 Pointers Category'),  # noqa: E501
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-3PTM",
                        children=[dcc.Graph(id="graph_3PTM")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Made 3 Pointers Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-3PTM-weekly",
                        children=[dcc.Graph(id="graph_3PTM_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
