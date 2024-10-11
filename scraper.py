import requests
import tweepy
from bs4 import BeautifulSoup
from utils.config import TEAM_STATS_URL
from utils.matchups import *
from utils.helpers import *
from keys import *

client = tweepy.Client(bearer_token, api_key, api_secret, access_token, access_token_secret)

auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth)

def get_team_stats(team):
    url = TEAM_STATS_URL.get(team.lower())

    current_week = get_current_game_week()
    if current_week is None:
        print(f"No active game week found for today's date.")
        return {}
    game_week = current_week - 1
    if not url:
        print(f"No URL found for {team}")
        return {}

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    sections = soup.find_all('h3', class_='nfl-o-teamstats__title')

    team_stats = {}

    for section in sections:
        title = section.text.strip()

        if title not in ["Passing", "Rushing", "Receiving"]:
            continue

        table = section.find_next('table')
        if not table:
            continue 

        stats = []
        table_rows = table.find_all('tr', {'aria-hidden': 'false'})

        for index, row in enumerate(table_rows):
            player_name = row.find('span', {'class': 'nfl-o-roster__player-name'}).text.strip()

            player_stats = {}
            if title == "Passing":
                pass_attempts = row.find_all('td')[1].text.strip()
                passing_yards = row.find_all('td')[3].text.strip()
                touchdowns = row.find_all('td')[6].text.strip()
                interceptions = row.find_all('td')[8].text.strip()

                pass_attempts = int(pass_attempts) if pass_attempts.isdigit() else 0
                passing_yards = int(passing_yards) if passing_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0
                interceptions = int(interceptions) if interceptions.isdigit() else 0

                pass_attempts_per_week = pass_attempts / game_week
                passing_yards_per_week = passing_yards / game_week
                touchdowns_per_week = touchdowns / game_week
                interceptions_per_week = interceptions / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Passing Attempts/Week": pass_attempts_per_week,
                    "Passing Yards/Week": passing_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week,
                    "Interceptions/Week": interceptions_per_week
                }

            elif title == "Rushing":
                rush_attempts = row.find_all('td')[1].text.strip()
                rushing_yards = row.find_all('td')[2].text.strip()
                touchdowns = row.find_all('td')[5].text.strip()

                rush_attempts = int(rush_attempts) if rush_attempts.isdigit() else 0
                rushing_yards = int(rushing_yards) if rushing_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0

                rush_attempts_per_week = rush_attempts / game_week
                rushing_yards_per_week = rushing_yards / game_week
                touchdowns_per_week = touchdowns / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Rushing Attempts/Week": rush_attempts_per_week,
                    "Rushing Yards/Week": rushing_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week
                }

            elif title == "Receiving":
                receptions = row.find_all('td')[1].text.strip()
                receiving_yards = row.find_all('td')[2].text.strip()
                touchdowns = row.find_all('td')[5].text.strip()

                receptions = int(receptions) if receptions.isdigit() else 0
                receiving_yards = int(receiving_yards) if receiving_yards.isdigit() else 0
                touchdowns = int(touchdowns) if touchdowns.isdigit() else 0

                receptions_per_week = receptions / game_week
                receiving_yards_per_week = receiving_yards / game_week
                touchdowns_per_week = touchdowns / game_week

                player_stats = {
                    "Player Name": player_name,
                    "Receptions/Week": receptions_per_week,
                    "Receiving Yards/Week": receiving_yards_per_week,
                    "Touchdowns/Week": touchdowns_per_week
                }

            stats.append(player_stats)
        team_stats[title] = stats

    return team_stats

current_week, current_matchups = get_current_week_matchups()

if current_week:
    print(f"\nProcessing matchups for Week {current_week}:\n")
    for team1, team2 in current_matchups:
        output = f"Weekly Average Stats for {team1.capitalize()} vs. {team2.capitalize()}:\n\n"

        team1_stats = get_team_stats(team1)
        team2_stats = get_team_stats(team2)

        output += f"{team1.capitalize()} Stats:\n"
        for category, players in team1_stats.items():
            output += f"\n{category}:\n"
            for player in players:
                output += f"- {player['Player Name']}: "
                output += ", ".join([f"{key}: {value}" for key, value in player.items() if key != "Player Name"]) + "\n"

        output += f"\n{team2.capitalize()} Stats:\n"
        for category, players in team2_stats.items():
            output += f"\n{category}:\n"
            for player in players:
                output += f"- {player['Player Name']}: "
                output += ", ".join([f"{key}: {value}" for key, value in player.items() if key != "Player Name"]) + "\n"

        print(output)
else:
    print("No matchups found for the current date.")

# client.create_tweet(text="STANDBY WE COOKING WEEK 6")