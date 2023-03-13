import dash
import copy

from dash import dcc, html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc

import plotly.express as px
import plotly.graph_objects as go

from data_generator import LeagueStats, NINE_CAT_CATEGORIES

from layout_files.points_plots import POINTS_LAYOUT
from layout_files.assist_plots import ASSISTS_LAYOUT
from layout_files.blocks_plots import BLOCKS_LAYOUT
from layout_files.field_goal_percent_plots import FIELD_GOAL_PERCENT_LAYOUT
from layout_files.free_throw_percent_plots import FREE_THROW_PERCENT_LAYOUT
from layout_files.rebounds_plots import REBOUNDS_LAYOUT
from layout_files.steals_plots import STEALS_LAYOUT
from layout_files.three_point_field_goal_plots import THREE_POINT_FIELD_GOALS_LAYOUT  # noqa: E501
from layout_files.turnovers_plots import TURNOVERS_LAYOUT


app = dash.Dash(
    external_stylesheets=[dbc.themes.LUMEN]
)

app.layout = dbc.Container(
    children=[
        html.H1(
            children='NBA Fantasy Basketball 9CAT League Analyzer',
            style={'textAlign': 'center', 'background-color': 'primary'}
        ),
        dbc.NavbarSimple(
            brand='Created by bleebop',
            brand_href='https://github.com/bleepbop?tab=repositories',
            color="primary",
            dark=True,
            className='mx-1'
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        dbc.Label(
                            'Search For Your ESPN League',
                            className='p-3'),
                    ])
                ),
                dbc.Col(
                    html.Div([
                        dbc.Label(
                            'Enter your ESPN League ID:  ',
                            className='p-3'
                        ),
                        dcc.Input(
                            id="input_league_id",
                            type="number",
                            placeholder="ESPN League ID"
                        )
                    ])
                ),
                dbc.Col(
                    html.Div([
                        dbc.Label(
                            'Enter your ESPN League Year:  ',
                            className='p-3'
                        ),
                        dcc.Input(
                            id="input_league_year",
                            type="number",
                            placeholder="Fantasy League Year"
                        )
                    ]),
                )
            ],
            className='bg-primary mx-1'
        ),
        dcc.Tabs(id='tabs', value='H2HTab', children=[
            dcc.Tab(
                label='Head to Head Comparison',
                id='h2h_tab',
                value='H2HTab',
                children=[
                    html.H2('Compare Teams Head to Head'),
                    html.Hr(),
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dbc.DropdownMenu(
                                        label="Team 1",
                                        id="team_1_selection",
                                        children=[]
                                    ),
                                    html.Plaintext()
                                ]
                            ),
                            dbc.Col(
                                [
                                    dbc.DropdownMenu(
                                        label="Team 2",
                                        id="team_2_selection",
                                        children=[]
                                    ),
                                    html.Plaintext()
                                ]
                            )
                        ]
                    )
                ]
            ),
            dcc.Tab(
                label='Points Plots',
                id='pts_tab',
                value='PtsTab',
                children=POINTS_LAYOUT
            ),
            dcc.Tab(
                label='Rebound Plots',
                id='reb_tab',
                value='RebTab',
                children=REBOUNDS_LAYOUT
            ),
            dcc.Tab(
                label='Assist Plots',
                id='ast_tab',
                value='AstTab',
                children=ASSISTS_LAYOUT
            ),
            dcc.Tab(
                label='Steal Plots',
                id='stl_tab',
                value='StlTab',
                children=STEALS_LAYOUT
            ),
            dcc.Tab(
                label='Block Plots',
                id='blk_tab',
                value='BlkTab',
                children=BLOCKS_LAYOUT
            ),
            dcc.Tab(
                label='Turnover Plots',
                id='to_tab',
                value='TOTab',
                children=TURNOVERS_LAYOUT
            ),
            dcc.Tab(
                label='Field Goal % Plots',
                id='fg_tab',
                value='FGTab',
                children=FIELD_GOAL_PERCENT_LAYOUT
            ),
            dcc.Tab(
                label='Free Throw % Plots',
                id='ft_tab',
                value='FTTab',
                children=FREE_THROW_PERCENT_LAYOUT
            ),
            dcc.Tab(
                label='3 Pointers Made Plots',
                id='3ptm_tab',
                value='3PTTab',
                children=THREE_POINT_FIELD_GOALS_LAYOUT
            )
        ]),
    ],
    fluid=True
)


@app.callback(
    Output(component_id='team_1_selection', component_property='children'),
    Output(component_id='team_2_selection', component_property='children'),
    Input(component_id='input_league_id', component_property='value'),
    Input(component_id='input_league_year', component_property='value'),
)
def init_team_dropdowns(league_id, league_year):
    if league_id is None or league_year is None:
        return
    my_league = LeagueStats(league_id, league_year)
    team_list = []
    for team in my_league.get_teams():
        team_list.append(
            dbc.DropdownMenuItem(team.team_name)
        )
    return team_list, copy.deepcopy(team_list)


@app.callback(
    Input(component_id='team_1_selection', component_property='value')
)
def analyze_team_1(self, team_name):
    pass


@app.callback(
    Input(component_id='team_2_selection', component_property='value')
)
def analyze_team_2(self, team_name):
    pass


@app.callback(
    Output(component_id='avg_pts', component_property='figure'),
    Output(component_id='avg_REB', component_property='figure'),
    Output(component_id='avg_AST', component_property='figure'),
    Output(component_id='avg_STL', component_property='figure'),
    Output(component_id='avg_BLK', component_property='figure'),
    Output(component_id='avg_TO', component_property='figure'),
    Output(component_id='avg_FG', component_property='figure'),
    Output(component_id='avg_FT', component_property='figure'),
    Output(component_id='avg_3PTM', component_property='figure'),
    Input(component_id='input_league_id', component_property='value'),
    Input(component_id='input_league_year', component_property='value'),
)
def init_weekly_avg_plots(league_id, league_year):
    if league_id is None or league_year is None:
        return
    my_league = LeagueStats(league_id, league_year)
    stats = my_league.rate_teams()
    total_cat_wins_df, weekly_performance_df = my_league.compute_categories_won()  # noqa: E501
    stats.set_index('TEAM_NAME')

    weekly_avgs_dict = {CAT: px.bar(stats, x="TEAM_NAME", y=CAT, color="TEAM_NAME") for CAT in NINE_CAT_CATEGORIES}  # noqa: E501
    return weekly_avgs_dict['PTS'], weekly_avgs_dict['REB'], weekly_avgs_dict['AST'], weekly_avgs_dict['STL'], weekly_avgs_dict['BLK'], weekly_avgs_dict['TO'], weekly_avgs_dict['FG%'], weekly_avgs_dict['FT%'], weekly_avgs_dict['3PTM']  # noqa: E501


@app.callback(
    Output(component_id='graph_pts', component_property='figure'),
    Output(component_id='graph_REB', component_property='figure'),
    Output(component_id='graph_AST', component_property='figure'),
    Output(component_id='graph_STL', component_property='figure'),
    Output(component_id='graph_BLK', component_property='figure'),
    Output(component_id='graph_TO', component_property='figure'),
    Output(component_id='graph_FG', component_property='figure'),
    Output(component_id='graph_FT', component_property='figure'),
    Output(component_id='graph_3PTM', component_property='figure'),
    Input(component_id='input_league_id', component_property='value'),
    Input(component_id='input_league_year', component_property='value'),
)
def init_weeks_won_plots(league_id, league_year):
    if league_id is None or league_year is None:
        return
    my_league = LeagueStats(league_id, league_year)
    total_cat_wins_df, weekly_performance_df = my_league.compute_categories_won()  # noqa: E501

    fig_dict = {CAT: px.bar(total_cat_wins_df, x="TEAM", y=CAT, color="TEAM") for CAT in NINE_CAT_CATEGORIES}  # noqa: E501
    return fig_dict['PTS'], fig_dict['REB'], fig_dict['AST'], fig_dict['STL'], fig_dict['BLK'], fig_dict['TO'], fig_dict['FG%'], fig_dict['FT%'], fig_dict['3PTM']  # noqa: E501


@app.callback(
    Output(component_id='graph_pts_weekly', component_property='figure'),
    Output(component_id='graph_REB_weekly', component_property='figure'),
    Output(component_id='graph_AST_weekly', component_property='figure'),
    Output(component_id='graph_STL_weekly', component_property='figure'),
    Output(component_id='graph_BLK_weekly', component_property='figure'),
    Output(component_id='graph_TO_weekly', component_property='figure'),
    Output(component_id='graph_FG_weekly', component_property='figure'),
    Output(component_id='graph_FT_weekly', component_property='figure'),
    Output(component_id='graph_3PTM_weekly', component_property='figure'),
    Input(component_id='input_league_id', component_property='value'),
    Input(component_id='input_league_year', component_property='value'),
)
def init_season_performance_plots(league_id, league_year):
    if league_id is None or league_year is None:
        return
    my_league = LeagueStats(league_id, league_year)
    total_cat_wins_df, weekly_performance_df = my_league.compute_categories_won()  # noqa: E501

    performance_per_week_dict = {}

    for CAT in NINE_CAT_CATEGORIES:
        weeks = weekly_performance_df[CAT]['week']
        fig = go.Figure()
        for team in my_league.league.teams:
            team_name = team.team_name
            cat_stats = weekly_performance_df[CAT][team_name]
            fig.add_trace(go.Scatter(name=team_name, x=weeks, y=cat_stats))
        fig.update_xaxes(title_text="Week")
        fig.update_yaxes(title_text=CAT)
        performance_per_week_dict[CAT] = fig
    return performance_per_week_dict['PTS'], performance_per_week_dict['REB'], performance_per_week_dict['AST'], performance_per_week_dict['STL'], performance_per_week_dict['BLK'], performance_per_week_dict['TO'], performance_per_week_dict['FG%'], performance_per_week_dict['FT%'], performance_per_week_dict['3PTM']  # noqa: E501


app.run_server(host='0.0.0.0', port=8000)
