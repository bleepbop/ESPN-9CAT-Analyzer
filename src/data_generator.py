from nba_api.stats.endpoints import LeagueDashPlayerStats
from nba_api.stats.static import players
from espn_api.basketball import League
from pandas import DataFrame

import numpy
import json
import pandas as pd
import math


CATEGORIES = ['PTS', 'FGM', 'FGA', 'FTM', 'FTA', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FG_PCT', 'FT_PCT', 'FG3M']
PERCENTAGE_CATEGORIES = ['FG', 'FT']
NINE_CAT_CATEGORIES = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TO', 'FG%', 'FT%', '3PTM']

class LeagueStats:
    '''
    Represents player/team stats for a given ESPN fantasy league during the specified season.
    '''
    def __init__(self, league_id=None, league_year=2023):
        self.league_id = league_id
        self.league_year = league_year
        self.season = str(league_year - 1) + '-' + str(league_year)[-2:]
        self.league = self.init_fantasy_league(self.league_id, self.league_year)

    def truncate(self, number, digits) -> float:
        '''
        Truncates number to specified number of digits.
        '''
        stepper = 10.0 ** digits
        return math.trunc(stepper * number) / stepper

    def create_active_players_df(self):
        '''
        Returns dataframe containing official names of all currrent active players.
        '''
        all_players = players.get_active_players()
        df = pd.DataFrame(all_players)
        df.rename(columns={'full_name': 'Player'}, inplace=True)
        pid_df = df[['id', 'Player']]
        return pid_df

    def compute_9cat_rankings(self):
        '''
        Computes 9CAT rankings for current season.
        '''
        player_stats = LeagueDashPlayerStats(season=self.season).league_dash_player_stats.get_data_frame()
        self.normalize_category_stats(player_stats)
        self.compute_category_leaders(player_stats)
        self.drop_columns(player_stats)
        category_coverage_players = self.average_ranking(player_stats)
        return player_stats, category_coverage_players

    def normalize_category_stats(self, stats: DataFrame):
        '''
        Computes player stats on a per-game basis.
        '''
        for index, player in stats.iterrows():
            games_played = player['GP']
            for category in CATEGORIES:
                if category not in ['FG_PCT', 'FT_PCT']:
                    stats.at[index, category] = player[category] / games_played

    def compute_category_leaders(self, stats: DataFrame):
        '''
        Sorts categories values by ascending (or descending for TOs) to determine leaders.
        '''
        for category in CATEGORIES:
            sorted_ascending = True if category == 'TOV' else False
            stats = stats.sort_values(by=category, ascending=sorted_ascending)
            stats = stats.reset_index(drop=True)
            ranking_key = category.upper() + '_RANK'
            stats[ranking_key] = stats.index

    def drop_columns(self, stats: DataFrame):
        '''
        Removes unnecessary columns from stats DataFrame object.
        '''
        all_columns = stats.columns
        for column in all_columns:
            if column in CATEGORIES or column[:-5] in CATEGORIES or column in ['PLAYER_ID', 'PLAYER_NAME']:
                continue
            del stats[column]

    def average_ranking(self, stats: DataFrame):
        '''
        Determine's a players average 9CAT ranking across all categories.
        Additionally stores the categories that a player is "Elite" in (ranking within the top 25).
        '''
        category_coverage_players = {}
        for index, player in stats.iterrows():
            sum = 0
            elite_category_names = []
            for category in CATEGORIES:
                rank = player[category + '_RANK']
                sum += rank
                if rank < 25:
                    elite_category_names.append(category)
            stats.at[index, 'TOTAL_RANK'] = sum / len(CATEGORIES)
            stats.at[index, 'NUM_ELITE_CATEGORIES'] = len(elite_category_names)
            category_coverage_players[player['PLAYER_NAME']] = elite_category_names
        return category_coverage_players

    def init_fantasy_league(self, league_id=None, league_year=2023):
        '''
        Initializes fantasy league with new League object. Stores pulled data to json file for future use.
        '''
        if league_id == None or league_year == None:
            return
        league = League(league_id, league_year)
        data_storage = {}
        
        for team in league.teams:
            player_names = [player.name for player in team.roster]
            data_storage[team.team_name] = player_names
        
        # For offline use
        with open('bubble_2_rosters.json', 'w') as fp:
            json.dump(data_storage, fp)
        
        return league

    def rate_teams(self):
        '''
        Rates each team's weekly performance in all categories.
        Assumes players play 3 games per week.
        '''
        player_stats, category_coverage_players = self.compute_9cat_rankings()
        f = open('bubble_2_rosters.json')
        data = json.load(f)
        f.close()
        all_teams = []
        for team in data:
            team_stats = {category: 0 for category in CATEGORIES}
            team_stats['TEAM_NAME'] = team
            for player in data[team]:
                indiv_stats = player_stats.loc[player_stats['PLAYER_NAME'] == player]
                for category in CATEGORIES:
                    if len(indiv_stats[category].values) and indiv_stats[category].values[0]:
                        team_stats[category] += (indiv_stats[category].values[0] * 3) # assume 3 game week
            for category in PERCENTAGE_CATEGORIES:
                pct_category_name = category + '_PCT'  # this will be either 'FG_PCT' or 'FT_PCT'
                category_makes = category + 'M'
                category_attempts = category + 'A'
                team_stats[pct_category_name] = self.truncate(team_stats[category_makes] / team_stats[category_attempts], 6)
            all_teams.append(team_stats)
        combined_df = pd.DataFrame(all_teams)
        combined_df.to_csv('computed_team_stats.csv', encoding='utf-8', index=True)
        for column in ['FGM', 'FGA', 'FTM', 'FTA']:  # Delete these now that team percentages have been calculated
            del combined_df[column]
        combined_df.rename(columns = {'TOV':'TO'}, inplace = True)
        combined_df.rename(columns = {'FG_PCT':'FG%'}, inplace = True)
        combined_df.rename(columns = {'FT_PCT':'FT%'}, inplace = True)
        combined_df.rename(columns = {'FG3M':'3PTM'}, inplace = True)
        return combined_df

    def compute_categories_won(self):
        '''
        Computes categories each team has won for each week of the current season.
        '''
        inner = {week: {} for week in range(1, 24)}
        categories_won_by_week = {str(team.team_id): {"team_name": team.team_name, "cats": inner.copy()} for team in self.league.teams}
        for week in range(0, 18):
            for matchup in self.league.scoreboard(week):
                # Prevent Errors for matchups that haven't occurred yet
                if matchup.home_team_cats and matchup.away_team_cats:
                    categories_won_by_week[str(matchup.home_team.team_id)]["cats"][week] = [entry for entry in matchup.home_team_cats.keys() if matchup.home_team_cats[entry]['result'] == 'WIN']
                    categories_won_by_week[str(matchup.away_team.team_id)]["cats"][week] = [entry for entry in matchup.away_team_cats.keys() if matchup.away_team_cats[entry]['result'] == 'WIN']
        
        cleaned_output = {}
        best_categories_by_team = []
        for id in categories_won_by_week:
            team_name = categories_won_by_week[id]["team_name"]
            new_dict = {team_name: categories_won_by_week[id]["cats"]}
            cleaned_output.update(new_dict)
            print(cleaned_output)
            team_name = categories_won_by_week[id]["team_name"]
            inner = {category: 0 for category in NINE_CAT_CATEGORIES}
            for week in new_dict[team_name]:
                for category in new_dict[team_name][week]:
                    inner[category] += 1
            inner.update({'TEAM': team_name})
            best_categories_by_team.append(inner)
        with open('categories_won.json', 'w') as fp:
            json.dump(cleaned_output, fp)
        with open('total_categories_won.json', 'w') as fp:
            json.dump(best_categories_by_team, fp)
        return pd.DataFrame.from_dict(best_categories_by_team)
