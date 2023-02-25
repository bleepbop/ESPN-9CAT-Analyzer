import dash
from dash import dash_table, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from espn_api.basketball import League
import plotly.express as px
import plotly.graph_objects as go

from data_generator import LeagueStats, NINE_CAT_CATEGORIES


my_league = LeagueStats(league_id='', league_year=2023)
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
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.Row(
                                [
                                    dbc.Label('Search For Your ESPN League'),
                                    html.Br(),
                                    dcc.Input(
                                        id="input_league_id",
                                        type="number",
                                        placeholder="ESPN League ID",
                                        persistence=True
                                    ),
                                    html.Br(),
                                    dcc.Input(
                                        id="input_league_year",
                                        type="number",
                                        placeholder="Fantasy League Year",
                                        persistence=True
                                    )
                                ]
                            ),
                        ],
                        body=True,
                        color='primary'
                    ),
                    md=4
                )
            ]
        ),
        dcc.Tabs(id='tabs', value='Tab1', children=[
            dcc.Tab(label='Points Plots', id='pts_tab', value='PtsTab', children =[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Points per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_pts", figure=weekly_avgs_dict['PTS'])
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
                                dcc.Graph(id="graph_pts", figure=fig_dict['PTS'])
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
                                dcc.Graph(id="graph_pts_weekly", figure=performance_per_week_dict['PTS'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Rebound Plots', id='reb_tab', value='RebTab', children=[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Rebounds per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_REB", figure=weekly_avgs_dict['REB'])
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
                                dcc.Graph(id="graph_REB", figure=fig_dict['REB'])
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
                                dcc.Graph(id="graph_REB_weekly", figure=performance_per_week_dict['REB'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Assist Plots', id='ast_tab', value='AstTab', children =[
                html.Hr(),
                html.Hr(),
                html.H2('Weekly Assist Averages per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_AST", figure=weekly_avgs_dict['AST'])
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
                                dcc.Graph(id="graph_AST", figure=fig_dict['AST'])
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
                                dcc.Graph(id="graph_AST_weekly", figure=performance_per_week_dict['AST'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Steal Plots', id='stl_tab', value='StlTab', children=[
                html.Hr(),
                html.Hr(),
                html.H2('Weekly Steal Averages per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_STL", figure=weekly_avgs_dict['STL'])
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
                                dcc.Graph(id="graph_STL", figure=fig_dict['STL'])
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
                                dcc.Graph(id="graph_STL_weekly", figure=performance_per_week_dict['STL'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Block Plots', id='blk_tab', value='BlkTab', children =[
                html.Hr(),
                html.Hr(),
                html.H2('Weekly Block Averages per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_BLK", figure=weekly_avgs_dict['BLK'])
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
                                dcc.Graph(id="graph_BLK", figure=fig_dict['BLK'])
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
                                dcc.Graph(id="graph_BLK_weekly", figure=performance_per_week_dict['BLK'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Turnover Plots', id='to_tab', value='TOTab', children=[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Turnovers per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_TO", figure=weekly_avgs_dict['TO'])
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
                                dcc.Graph(id="graph_TO", figure=fig_dict['TO'])
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
                                dcc.Graph(id="graph_TO_weekly", figure=performance_per_week_dict['TO'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Field Goal % Plots', id='fg_tab', value='FGTab', children =[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Field Goal Percent per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_FG", figure=weekly_avgs_dict['FG%'])
                            ]
                        )
                    ]
                ),
                html.Hr(),
                html.H2('# Of Weeks Each Team Has Won Field Goal Percentage Category'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="graph_FG", figure=fig_dict['FG%'])
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
                                dcc.Graph(id="graph_FG_weekly", figure=performance_per_week_dict['FG%'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='Free Throw % Plots', id='ft_tab', value='FTTab', children=[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Free Throw Percentage per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_FT", figure=weekly_avgs_dict['FT%'])
                            ]
                        )
                    ]
                ),
                html.Hr(),
                html.H2('# Of Weeks Each Team Has Won Free Throw Percentage Category'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="graph_FT", figure=fig_dict['FT%'])
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
                                dcc.Graph(id="graph_FT_weekly", figure=performance_per_week_dict['FT%'])
                            ]
                        )
                    ]
                ),
            ]),
            dcc.Tab(label='3 Pointers Made Plots', id='3ptm_tab', value='3PTTab', children =[
                html.Hr(),
                html.Hr(),
                html.H2('Average Weekly Made 3 Pointers per Team'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="avg_3PTM", figure=weekly_avgs_dict['3PTM'])
                            ]
                        )
                    ]
                ),
                html.Hr(),
                html.H2('# Of Weeks Each Team Has Won Made 3 Pointers Category'),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Graph(id="graph_3PTM", figure=fig_dict['3PTM'])
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
                                dcc.Graph(id="graph_3PTM_weekly", figure=performance_per_week_dict['3PTM'])
                            ]
                        )
                    ]
                )
            ])
        ]),
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
