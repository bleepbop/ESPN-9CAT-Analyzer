# ESPN-9CAT-Analyzer
Dash graphs for viewing head-to-head matchup stats between teams in a ESPN 9CAT league.

You'll need the ID for your ESPN league. This can be retrieved from the 'League Home' URL:

ex: `https://fantasy.espn.com/basketball/league?leagueId=<copy_this_league_id>`

Make sure that your league is public and viewable. This can be done by:
* Navigating to `League Settings`
* Clicking `Basic Settings`
* Setting `Make League Viewable to Public` to true

The program will take the input year and input league ID on the main page.

## Running the program
From the main directory (`9CAT_RANKINGS`):
*Note: It is recommended to use a virtual environment such as venv for this*

1. `pip install -r requirements.txt`

2. `python3 src/dash_graphs.py`

and navigate to `http://localhost:8000` in the browser.

### Running the App with Docker
Build the image: 

`docker build -t nbaplots .`

Run the container on port 8000:

`docker run -p 8000:8000 -d nbaplots`
