import dash_bootstrap_components as dbc

from dash import dcc, html


FREE_THROW_PERCENT_LAYOUT = [
    html.H2('Average Weekly Free Throw Percentage per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-FT",
                        children=[dcc.Graph(id="avg_FT")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Free Throw Percentage Category'),  # noqa: E501
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-FT",
                        children=[dcc.Graph(id="graph_FT")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Free Throw Percentage Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-FT-weekly",
                        children=[dcc.Graph(id="graph_FT_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
