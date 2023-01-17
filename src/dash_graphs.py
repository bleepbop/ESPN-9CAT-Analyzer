import dash
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from espn_api.basketball import League
import plotly.express as px
import plotly.graph_objects as go

from data_generator import LeagueStats, NINE_CAT_CATEGORIES


my_league = LeagueStats()
stats = my_league.rate_teams()
total_cat_wins_df, weekly_performance_df = my_league.compute_categories_won()
stats.set_index('TEAM_NAME')

fig_dict = {CAT: px.bar(total_cat_wins_df, x="TEAM", y=CAT, color="TEAM") for CAT in NINE_CAT_CATEGORIES}
weekly_avgs_dict = {CAT: px.bar(stats, x="TEAM_NAME", y=CAT, color="TEAM_NAME") for CAT in NINE_CAT_CATEGORIES}
performance_per_week_dict = {}

for CAT in NINE_CAT_CATEGORIES:
    weeks = weekly_performance_df[CAT]['week']
    fig = go.Figure()
    for team in my_league.league.teams:
        team_name = team.team_name
        cat_stats = weekly_performance_df[CAT][team_name]
        fig.add_trace(go.Line(name=team_name, x=weeks, y=cat_stats))
    fig.update_xaxes(title_text="Week")
    fig.update_yaxes(title_text=CAT)
    performance_per_week_dict[CAT] = fig


app = dash.Dash(
    external_stylesheets=[dbc.themes.LUMEN]
)

app.layout = dbc.Container(
    children=[
        html.H1(children='NBA Fantasy Basketball 9CAT League Analyzer', style={'textAlign': 'center', 'background-color':'primary'}),
        dbc.NavbarSimple(
            brand='Created by bleebop',
            brand_href='https://github.com/bleepbop?tab=repositories',
            color="primary",
            dark=True,
        ),
        html.Hr(),
        html.Hr(),
        html.H2('Weekly Stat Averages per Team'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('PTS'),
                        dcc.Graph(id="avg_pts", figure=weekly_avgs_dict['PTS'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('AST'),
                        dcc.Graph(id="avg_AST", figure=weekly_avgs_dict['AST'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('STL'),
                        dcc.Graph(id="avg_STL", figure=weekly_avgs_dict['STL'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('BLK'),
                        dcc.Graph(id="avg_BLK", figure=weekly_avgs_dict['BLK'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('3PTM'),
                        dcc.Graph(id="avg_3PTM", figure=weekly_avgs_dict['3PTM'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('FG%'),
                        dcc.Graph(id="avg_FG", figure=weekly_avgs_dict['FG%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('FT%'),
                        dcc.Graph(id="avg_FT", figure=weekly_avgs_dict['FT%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('TO'),
                        dcc.Graph(id="avg_TO", figure=weekly_avgs_dict['TO'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('REB'),
                        dcc.Graph(id="avg_REB", figure=weekly_avgs_dict['REB'])
                    ]
                )
            ]
        ),
        html.Hr(),
        html.H2('# Of Weeks A Team Has Won Given Category'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('PTS'),
                        dcc.Graph(id="graph_pts", figure=fig_dict['PTS'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('REB'),
                        dcc.Graph(id="graph_REB", figure=fig_dict['REB'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('AST'),
                        dcc.Graph(id="graph_AST", figure=fig_dict['AST'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('STL'),
                        dcc.Graph(id="graph_STL", figure=fig_dict['STL'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('BLK'),
                        dcc.Graph(id="graph_BLK", figure=fig_dict['BLK'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('TO'),
                        dcc.Graph(id="graph_TO", figure=fig_dict['TO'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('FG%'),
                        dcc.Graph(id="graph_FG", figure=fig_dict['FG%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('FT%'),
                        dcc.Graph(id="graph_FT", figure=fig_dict['FT%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('3PTM'),
                        dcc.Graph(id="graph_3PTM", figure=fig_dict['3PTM'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('PTS per Week'),
                        dcc.Graph(id="graph_PTS_PER_WEEK", figure=fig_dict['3PTM'])
                    ]
                )
            ]
        ),
        html.Hr(),
        html.H2('Category Performance over Season'),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly PTS'),
                        dcc.Graph(id="graph_pts_weekly", figure=performance_per_week_dict['PTS'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly REB'),
                        dcc.Graph(id="graph_REB_weekly", figure=performance_per_week_dict['REB'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly AST'),
                        dcc.Graph(id="graph_AST_weekly", figure=performance_per_week_dict['AST'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly STL'),
                        dcc.Graph(id="graph_STL_weekly", figure=performance_per_week_dict['STL'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly BLK'),
                        dcc.Graph(id="graph_BLK_weekly", figure=performance_per_week_dict['BLK'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly TO'),
                        dcc.Graph(id="graph_TO_weekly", figure=performance_per_week_dict['TO'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly FG%'),
                        dcc.Graph(id="graph_FG_weekly", figure=performance_per_week_dict['FG%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly FT%'),
                        dcc.Graph(id="graph_FT_weekly", figure=performance_per_week_dict['FT%'])
                    ]
                )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.P('Weekly 3PTM'),
                        dcc.Graph(id="graph_3PTM_weekly", figure=performance_per_week_dict['3PTM'])
                    ]
                )
            ]
        )
    ],
    fluid=True
)


app.run_server(host='0.0.0.0', port=8000, debug=True)


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    return [{
        'if': { 'column_id': i },
        'background_color': '#D2F3FF'
    } for i in selected_columns]

@app.callback(
    Output("graph", "figure"), 
    [Input("categories", "value")])
def filter_heatmap(cols):
    data = stats.copy()

    fig = px.imshow(
        data=data,
        x=['PTS'],
        y=['TEAM_NAME']
    )
    return fig
