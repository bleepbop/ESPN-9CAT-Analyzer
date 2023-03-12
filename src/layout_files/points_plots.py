import dash_bootstrap_components as dbc

from dash import dcc, html


POINTS_LAYOUT = [
    html.H2('Average Weekly Points per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-pts",
                        children=[dcc.Graph(id="avg_pts")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Points Category'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-pts",
                        children=[dcc.Graph(id="graph_pts")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Points Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-pts-weekly",
                        children=[dcc.Graph(id="graph_pts_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
]
