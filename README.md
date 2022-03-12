# ESPN-9CAT-Analyzer
Dash graphs for viewing head-to-head matchup stats between teams in a ESPN 9CAT league.

You'll need the ID for your ESPN league. This can be retrieved from the 'League Home' URL:
ex: `https://fantasy.espn.com/basketball/league?leagueId=<copy_this_league_id>`

Make sure that your league is public and viewable. This can be done by:
* Navigating to `League Settings`
* Clicking `Basic Settings`
* Setting `Make League Viewable to Public` to true

Then, enter the league ID as the `league_id` parameter in `LeagueStats.__init__` in `data_generator.py`.

Finally, run the program

`python3 dash_graphs.py`

and navigate to `http://localhost:8000` in the browser.
