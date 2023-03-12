import dash_bootstrap_components as dbc

from dash import dcc, html


FIELD_GOAL_PERCENT_LAYOUT = [
    html.H2('Average Weekly Field Goal Percent per Team'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-avg-FG",
                        children=[dcc.Graph(id="avg_FG")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('# Of Weeks Each Team Has Won Field Goal Percentage Category'),  # noqa: E501
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-FG",
                        children=[dcc.Graph(id="graph_FG")],
                        type="graph",
                    )
                ]
            )
        ]
    ),
    html.Hr(),
    html.H2('Field Goal Percentage Per Week'),
    dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Loading(
                        id="loading-graph-FG-weekly",
                        children=[dcc.Graph(id="graph_FG_weekly")],
                        type="graph",
                    )
                ]
            )
        ]
    )
]
